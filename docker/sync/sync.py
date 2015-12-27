#!/usr/bin/env python3

""" I generate and overwrite the following configurations:

- /etc/aliases (smtpd)
- /etc/mailname (smtpd)
- /etc/smtpd.conf (smtpd)
- /etc/apache2/sites-available/roundcube.conf (roundcube)
"""

import configparser
import os
import shlex
import subprocess
import time


CONFIG_PATH = '/config.ini'
TARGET_PATH = '/confs'
SMTPD_TEMPLATE = '/smtpd.conf.template'


class MailzSync(object):
    """ I'm responsible of synchronizing confs.
    """
    def __init__(self):
        self.now = time.strftime("%c")
        self.config = configparser.RawConfigParser()
        self.config.read(CONFIG_PATH)

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

                if self.config.has_option('global', 'domain'):
                    hostname = self.config.get('global', 'domain')
                if not hostname:
                    hostname = os.getenv('DEFAULT_HOSTNAME')

                settings = {}
                settings['hostname'] = hostname

                output.write(template.format(**settings))


if __name__ == '__main__':
    m = MailzSync()
    m.sync_aliases()
    m.sync_users()
    m.sync_smtpd()

