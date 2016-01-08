# Docker Mailz

All-in-one solution to manage mails on a Linux box with a single,
simple, human-readable configuration file.

![](https://github.com/aimxhaisse/docker-mailz/raw/master/mailz/docker-mailz.png)

## Components

* OpenSMTPD
* SpamPD (SpamAssassin)
* Dovecot
* Sieve
* RoundCube

## Setup

    $ cp config.ini.example config.ini
    $ $EDITOR config.ini

## Usage

    $ make
    Mailz, lots of mailz.
    
    All configuration is done via config.ini, enjoy.
    
    spawn            sync configuration and respawn all containers
    logs             print containers logs
    backup           backup mail data
    stop             stop all containers
    encrypt          encrypt a password
    status           show status of containers
    help             print this help

## Features

* Multiple users
* SSL
* Webmail
* Antispam
* Backups

## How To

Everything is managed by `config.ini`, if you need:

* to change certificates
* add a user
* update a password
* remove a user
* change your hostname
* …

Edit `config.ini` and `make spawn`.
