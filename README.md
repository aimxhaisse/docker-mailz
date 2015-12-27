# Docker Mailz

Mails. Lots of mails.

## Setup

Make sure you have `Docker` and `docker-compose`, edit `config.ini`,
then:

    make

You now have:

- a SMTP server configured for your hostname forwarding mails to…
- an SPAM filter which forwards regular mails to…
- an IMAP server which is regularily polled by…
- a RoundCube web interface waiting for you

## Features

- multiple users
- aliases
- SSL
- antispam
- facilities to backup

## Common Tasks

All configuration is done through the `config.ini` file, if you want
to add a user, edit a password, change your domain name… Edit the file
and run `make`.

You can also edit template configuration files that are in
`mailz/templates` and re-run `make`.

If you need something else that can't be done in this way, consider
opening a ticket :-)

## Backups

    cp -r mailz/data backup-$(date +%s)

Or if you are lazy:

    make backup

This will stop all containers nicely, perform the backup, and restart
them. Backups are by default stored in `mailz/backups` (can be
configured in `config.ini`).

## SSL

By default, if you don't provide a `privkey` in the configuration
file, a key is generated for you.

Similarily, if you don't provide a `cert` in the configuration file,
a self-signed certificate is derived from `privkey`.

## Virtualhosts

Docker Mailz can be coupled with
[nginx-proxy](https://github.com/jwilder/nginx-proxy), if you already
have it, your RoundCube virtualhost should already be available.