Safehouse
===

Safehouse is a __headless__ (I didn't write any js or templates), __developer-focused__ (you config it by editing the source code), __scale-invariant__ (it only has one user) django server. You text it or (eventually) email it codewords and parameters, and it does stuff. Like send you a joke. Or text a bunch of your friends saying you're having a serious mental episode and need to talk to someone _right now_ before you cut off your hands.

There's a reason it's called Safehouse, I guess.

I've been developing the code as a personal defensive tool, but a couple of people have expressed interest in setting up copies for themselves, so I'm putting it online. The code is going through continuous mass rearchitecturing. This is my intro project to django and I'm alwats seeing stuff to fix.

To Use
----

0. Copy the code and set it up on a server. Use a venv because venv is nice. Make sure it's a pyvenv3.4. You can install all of the required packages with just `pip install -r requirements`.
1.  The code assumes you're using [Heroku](https://www.heroku.com/), but I think it should work on any other hosting. Note settings.py assumes postgres, so you'll have to modify it if you want to use MySQL.
2. Get a [Twilio](twilio.com) account, and point a number at {applocation}/sms/. This is your Safehouse number.
3. Add the config values for things in configvals.md.
4. Run python manage.py syncdb to create all of the tables. Add contacts with the django admin page ({applocation}/admin).
  * Because South 1.0.0 is broken for Python3 (as of 9/15/14), we use 0.8.3, which breaks twilio-django. I'm going to get this fixed as soon as possible (aka upgrade to django 1.7), but for now you _might_ have to delete the migration files in `venv/lib/python3.4/site-packages/django_twilio`.
5. Text the safehouse number command codes to do things.
  * See the 'routes' wiki page for more details on what you can text and how this works.
6. Yell at me for not writing full documentation on how to use the Notifier feature.

Future Changes
----

* Upgrade to django 1.7. That'll fix the Python3/South/Django-Twilio death triangle.
* Delayed messages would be pretty cool, I think. (Sort of implemented with saved message tags... ish.)
* Email functionality.
