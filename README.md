# Docker Mailz

Mails. Lots of mails.

## Setup

    make HOSTNAME=your_hostname
    docker-compose up -d

You now have:

- a SMTP server configured for your hostname forwarding mails to...
- an Spam filter which forwards valid emails to...
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
