# Docker Mailz

Mails. Lots of mails.

## Setup

    make

You now have:

- a SMTP server configured for your hostname forwarding mails to...
- an SPAM filter which forwards regular mails to...
- an IMAP server which is regularily polled by...
- a RoundCube web interface waiting for you

## Common Tasks

### Add aliases

    $EDITOR data/confs/aliases
    docker-compose restart

### Add users

    misc/add-user <username>

### Backups

    cp -r data backup-$(date +%s)
