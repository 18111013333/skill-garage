---
name: imap-smtp-email
description: Read and send email via IMAP/SMTP. Check for new/unread messages, fetch content, search mailboxes, mark as read/unread, and send emails with attachments. Supports multiple accounts. Works with any IMAP/SMTP server including Gmail, Outlook, 163.com, vip.163.com, 126.com, vip.126.com, 188.com, and vip.188.com.
metadata:
  openclaw:
    emoji: "📧"
    requires:
      bins:
        - node
        - npm
---

# IMAP/SMTP Email Tool

Read, search, and manage email via IMAP protocol. Send email via SMTP. Supports Gmail, Outlook, 163.com, vip.163.com, 126.com, vip.126.com, 188.com, vip.188.com, and any standard IMAP/SMTP server.

## Configuration

Run the setup script to configure your email account:

```bash
bash setup.sh
```

Configuration is stored at `~/.config/imap-smtp-email/.env` (survives skill updates). If no config is found there, the skill falls back to a `.env` file in the skill directory (for backward compatibility).

### Config file format

```bash
# Default account (no prefix)
IMAP_HOST=imap.gmail.com
IMAP_PORT=993
IMAP_USER=your@email.com
IMAP_PASS=your_password
IMAP_TLS=true
IMAP_REJECT_UNAUTHORIZED=true
IMAP_MAILBOX=INBOX

SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_SECURE=false
SMTP_USER=your@email.com
SMTP_PASS=your_password
SMTP_FROM=your@email.com
SMTP_REJECT_UNAUTHORIZED=true

# File access whitelist (security)
ALLOWED_READ_DIRS=~/Downloads,~/Documents
ALLOWED_WRITE_DIRS=~/Downloads
```

## Multi-Account

You can configure additional email accounts in the same config file. Each account uses a name prefix (uppercase) on all variables.

### Adding an account

Run the setup script and choose "Add a new account":

```bash
bash setup.sh
```

Or manually add prefixed variables to `~/.config/imap-smtp-email/.env`:

```bash
# Work account (WORK_ prefix)
WORK_IMAP_HOST=imap.company.com
WORK_IMAP_PORT=993
WORK_IMAP_USER=me@company.com
WORK_IMAP_PASS=password
WORK_IMAP_TLS=true
WORK_IMAP_REJECT_UNAUTHORIZED=true
WORK_IMAP_MAILBOX=INBOX
WORK_SMTP_HOST=smtp.company.com
WORK_SMTP_PORT=587
WORK_SMTP_SECURE=false
WORK_SMTP_USER=me@company.com
WORK_SMTP_PASS=password
WORK_SMTP_FROM=me@company.com

## 详细文档

请参阅 [references/details.md](references/details.md)
