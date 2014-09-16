The following convig values should be set for this all to work. You can set them locally with `export FOO=whatever`, and for Heroku you can use `heroku config:set FOO=whatever`.

* `MY_NAME` should be your first name, unless you mess with the code.
* `MY_NUMBER` determines whether Safehouse forwards a text to you or runs a command. Do not use hyphones or spaces and prefix it with a 1, aka instead of "(555)-666-7777" make it "15556667777".
* `TWILIO_ACCOUNT_ID` and `TWILIO_AUTH_TOKEN` are required for any sms functionality.
* `TWILIO_NUMBER` is required to send outgoing messages.
* `DJANGO_ENVIRONMENT` should be "production" to use postgres and disable debug, anything else to use SQLite and enable debug.
  * In production, set `DJANGO_DEBUG` to enable debug mode, unset it to disable it.
  * In production, setting `TWILIO_DEBUG` to anything will disable forgery protection, in case you want to hit your site through curl (and let other people do that, too.)
