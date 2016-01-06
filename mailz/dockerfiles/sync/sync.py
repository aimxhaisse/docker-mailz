#!/usr/bin/env python3

""" I generate and overwrite various configuration files.
"""

import configparser
import glob
import hashlib
import os
import shlex
import shutil
import subprocess
import time


CONFIG_PATH = '/config.ini'
TARGET_PATH = '/confs'


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
                        output.write('{0}: {1}\n'.format(alias, aliases[0]))

    def sync_userbase(self):
        """ I recreate the userbase file.
        """
        target = '{0}/userbase'.format(TARGET_PATH)
        with open(target, 'w') as output:
            for userlist, _ in self.config.items('users'):
                aliases = userlist.split(',')
                output.write('{0} 1000:100:/\n'.format(aliases[0]))

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
            for userlist, password in self.config.items('users'):
                login = userlist.split(',')[0]
                output.write('{0}:{1}:::::\n'.format(login, password))

    def sync_credentials(self):
        """ I recreate the users file.
        """
        target = '{0}/credentials'.format(TARGET_PATH)
        with open(target, 'w') as output:
            for userlist, password in self.config.items('users'):
                login = userlist.split(',')[0]
                output.write('{0}@{1} {2}\n'.format(login,
                                                    self.settings['hostname'],
                                                    password))

    def sync_templates(self):
        """ I synchronize all templates.
        """
        for path in glob.glob('/templates/*.template'):
            target = '{0}/{1}'.format(TARGET_PATH, os.path.basename(path)[:-9])
            with open(path, 'r') as input:
                template = input.read()
                with open(target, 'w') as output:
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
            with open(source, 'rb') as afile:
                source_sum = hashlib.md5(afile.read()).hexdigest()
            with open(target, 'rb') as afile:
                target_sum = hashlib.md5(afile.read()).hexdigest()
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
            with open(source, 'rb') as afile:
                source_sum = hashlib.md5(afile.read()).hexdigest()
            with open(target, 'rb') as afile:
                target_sum = hashlib.md5(afile.read()).hexdigest()
            if source_sum != target_sum:
                return self.do_copy(source, target)


if __name__ == '__main__':
    m = MailzSync()
    m.sync_templates()
    m.sync_aliases()
    m.sync_userbase()
    m.sync_mailname()
    m.sync_users()
    m.sync_credentials()
    force_cert_reload = m.sync_privkey()
    m.sync_cert(force=force_cert_reload)
