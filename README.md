# Docker Mailz

Mails. Lots of mails.

## Setup

Make sure you have `Docker`, edit `config.ini`, then:

    make

You now have:

- a SMTP server configured for your hostname forwarding mails to…
- an SPAM filter which forwards regular mails to…
- an IMAP server which is regularily polled by…
- a RoundCube web interface waiting for you

## Common Tasks

All configuration is done through the `config.ini` file, if you want
to add a user, edit a password, change your domain name… Edit the file
and run `make`.

## Backups

    cp -r data backup-$(date +%s)

## SSL

By default, if you don't provide a `ssl_privkey` in the configuration
file, a key is generated for you.

Similarily, if you don't provide a `ssl_cert` in the configuration file,
a self-signed certificate is derived from the private key.
