# Docker Mailz

Mailz. Lots of mailz.

All-in-one solution to manage mails on a Linux box.

## Components

* OpenSMTPD
* SpamPD (SpamAssassin)
* Dovecot
* RoundCube

## Usage

    $ make
    Mailz, lots of mailz.
    
    All configuration is done via config.ini, enjoy.
    
    spawn           sync configuration and respawn all containers
    logs            print containers logs
    backup          backup mail data
    stop            stop all containers
    encrypt         encrypt a password
    help            print this help

## Features

* Multiple users
* SSL
* Webmail
* Antispam
* Backups

## How To

Everything is managed by `config.ini`, if you need to change
certificates, add a user, update a password, remove a user… edit
`config.ini` then `make spawn`.
