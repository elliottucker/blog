Title: Working setup for sending email via Gmail from Emacs on OSX
Date: 2013-05-06 16:45
Tags: Emacs, Email, OSX


From what I'd read up getting email to send directly from Emacs was going to use up quite a bit of my life.  I thought it would be worthwhile as a quick way of sending snippets to colleagues so I thought I'd give it ago.  After a small amount of struggle I've got it.

## 1. Install gnutls

I've [Macports](http://macports.org) installed so this step is easy.
```
$ sudo port install gnutls
```

Once this is installed make a note of the path to the binary

```
$ which gnutls-cli
```

## 2. Create an emacs readable authfile

```
$ touch ~/.authinfo
$ chmod 600 ~/.authinfo
```

Edit this file to include your own Google credentials. If using 2-step authentication you'll need to create an application-specific password in your Google Accounts-Security settings for this.

```
machine smtp.gmail.com port 587 login YOURNAME@gmail.com password YOURPASS
```


## 3. Add the following to your .emacs file

```
(setq 
 send-mail-function 'smtpmail-send-it
 message-send-mail-function 'smtpmail-send-it
 user-mail-address "YOURNAME@gmail.com"
 smtpmail-starttls-credentials '(("smtp.gmail.com" "587" nil nil))
 smtpmail-auth-credentials  (expand-file-name "~/.authinfo")
 smtpmail-default-smtp-server "smtp.gmail.com"
 smtpmail-smtp-server "smtp.gmail.com"
 smtpmail-smtp-service 587
 smtpmail-debug-info t
 starttls-extra-arguments nil
 starttls-gnutls-program "/opt/local/bin/gnutls-cli"
 starttls-extra-arguments nil
 starttls-use-gnutls t
)
```

Replace the path in starttls-gnutls-program with the path noted in step 1.

Reload your .emacs file `M-x load-file RET RET` and you're good to go...with ```C-x m```
