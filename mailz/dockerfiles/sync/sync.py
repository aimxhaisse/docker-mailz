#!/usr/bin/env python3

""" I generate and overwrite various configuration files.
"""

import configparser
import hashlib
import os
import shlex
import shutil
import subprocess
import time


CONFIG_PATH = '/config.ini'
TARGET_PATH = '/confs'
SMTPD_TEMPLATE = '/templates/smtpd.conf.template'
VHOST_TEMPLATE = '/templates/virtualhost.template'
DOCKER_COMPOSE_TEMPLATE = '/templates/docker-compose.yml.template'
ROUNDCUBE_TEMPLATE = '/templates/roundcube.config.inc.php.template'


class MailzSync(object):
    """ I'm responsible of synchronizing confs.
    """
    def __init__(self):
        self.now = time.strftime("%c")
        self.config = configparser.RawConfigParser()
        self.config.read(CONFIG_PATH)

        if self.config.has_option('global', 'domain'):
            hostname = self.config.get('global', 'domain')
        if not hostname:
            hostname = os.getenv('DEFAULT_HOSTNAME')

        if self.config.has_option('global', 'virtualhost'):
            virtualhost = self.config.get('global', 'virtualhost')
        if not virtualhost:
            virtualhost = 'mail.{0}'.format(hostname)

        self.settings = {}
        self.settings['hostname'] = hostname
        self.settings['virtualhost'] = virtualhost
        self.settings['conf_dir'] = os.getenv('CONF_DIR')
        self.settings['data_dir'] = os.getenv('DATA_DIR')

    def sync_aliases(self):
        """ I recreate the aliases file.
        """
        target = '{0}/aliases'.format(TARGET_PATH)
        with open(target, 'w') as output:
            output.write('# Generated on {0}\n\n'.format(self.now))
            for userlist, _ in self.config.items('users'):
                aliases = userlist.split(',')
                if len(aliases) > 1:
                    for alias in aliases[1:]:
                        output.write('{0}: {1}\n'.format(aliases[0], alias))

    def sync_mailname(self):
        """ I create the mailname file.
        """
        target = '{0}/mailname'.format(TARGET_PATH)
        with open(target, 'w') as output:
            output.write('{0}\n'.format(self.settings['hostname']))

    def sync_users(self):
        """ I recreate the users file.
        """
        target = '{0}/users'.format(TARGET_PATH)
        with open(target, 'w') as output:
            output.write('# Generated on {0}\n\n'.format(self.now))
            for userlist, clear_password in self.config.items('users'):
                login = userlist.split(',')[0]
                cmd = 'smtpctl encrypt {0}'.format(shlex.quote(clear_password))
                password = subprocess.check_output(cmd, shell=True)
                password = password.decode().strip()
                output.write('{0}:{1}:::::\n'.format(login, str(password)))

    def sync_smtpd(self):
        """ I synchronize opensmtpd's configuration file.
        """
        with open(SMTPD_TEMPLATE, 'r') as input:
            template = input.read()
            with open('{0}/smtpd.conf'.format(TARGET_PATH), 'w') as output:
                output.write('# Generated on {0}\n\n'.format(self.now))
                output.write(template.format(**self.settings))

    def sync_docker_compose(self):
        """ I synchronize docker-compose.yml file.
        """
        with open(DOCKER_COMPOSE_TEMPLATE, 'r') as input:
            template = input.read()
            with open('{0}/docker-compose.yml'.format(
                    TARGET_PATH), 'w') as output:
                output.write('# Generated on {0}\n\n'.format(self.now))
                output.write(template.format(**self.settings))

    def sync_roundcube(self):
        """ I synchronize roundcube config file.
        """
        with open(ROUNDCUBE_TEMPLATE, 'r') as input:
            template = input.read()
            with open('{0}/roundcube.config.inc.php'.format(
                    TARGET_PATH), 'w') as output:
                output.write('<?php // Generated on {0} ?>\n'.format(self.now))
                output.write(template.format(**self.settings))

    def sync_vhost(self):
        """ I synchronize virtualhost's configuration file.
        """
        with open(VHOST_TEMPLATE, 'r') as input:
            template = input.read()
            with open('{0}/virtualhost.conf'.format(
                    TARGET_PATH), 'w') as output:
                output.write('# Generated on {0}\n\n'.format(self.now))
                output.write(template.format(**self.settings))

    def do_copy(self, source, target):
        """ Simply overwrite the file.
        """
        shutil.copyfile(source, target)
        return True

    def do_gen_privkey(self, target):
        """ Generates a private key.
        """
        cmd = 'openssl genrsa -out {0} 4096'.format(target)
        subprocess.check_call(cmd, shell=True)
        return True

    def do_gen_cert(self, privkey, output):
        """ Generates a self-signed certificate.
        """
        cmd = 'echo -e "\\n\\n\\n\\n{0}\\n\\n\\n" '
        cmd += ' | '
        cmd += 'openssl req -new -x509 -key {1} -out {2}'
        cmd = cmd.format(self.settings['hostname'], privkey, output)
        subprocess.check_call(cmd, shell=True)

    def sync_cert(self, force):
        """ I synchronize the certificate of generate a self-signed one.
        """
        privkey = '{0}/privkey.pem'.format(TARGET_PATH)
        target = '{0}/cert.pem'.format(TARGET_PATH)
        source = '/cert.pem'
        if force:
            return self.do_gen_cert(privkey, target)
        if not os.path.exists(target):
            if os.path.exists(source):
                return self.do_copy(source, target)
            return self.do_gen_cert(privkey, target)
        if os.path.exists(source):
            source_sum = hashlib.md5(source).hexdigest()
            target_sum = hashlib.md5(target).hexdigest()
            if source_sum != target_sum:
                return self.do_copy(source, target)

    def sync_privkey(self):
        """ I synchronize the private key or generate a new one.
        """
        target = '{0}/privkey.pem'.format(TARGET_PATH)
        source = '/privkey.pem'

        if not os.path.exists(target):
            if os.path.exists(source):
                return self.do_copy(source, target)
            return self.do_gen_privkey(target)
        if os.path.exists(source):
            source_sum = hashlib.md5(source).hexdigest()
            target_sum = hashlib.md5(target).hexdigest()
            if source_sum != target_sum:
                return self.do_copy(source, target)


if __name__ == '__main__':
    m = MailzSync()
    m.sync_aliases()
    m.sync_mailname()
    m.sync_users()
    m.sync_docker_compose()
    m.sync_smtpd()
    m.sync_vhost()
    force_cert_reload = m.sync_privkey()
    m.sync_cert(force=force_cert_reload)
    m.sync_roundcube()
