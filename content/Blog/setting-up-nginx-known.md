Title: Setting up Known with Nginx
Slug: setting-up-known-with-nginx-indieweb
Date: 2015-03-05 08:49:39
Tags: Nginx, indieweb

[Known](http://withknown.com) is the soon to be released open source blogging platform that has built-in "IndieWeb" features such as webmentions, POSSE (Publish On your Own Site Syndicate Elsewhere) and the ability to use yor own site as login mechanism for other IndieWeb compliant sites. For more info on IndieWeb check out http://indiewebcamp.com.

Known is due to be released "this summer" but the [pre-releases source code is available on GitHub](https://github.com/idno/idno) so I thought I'd have a tinker. Much of my tinkering is likely to be made redundant by the time they release but never mind, it's all good practice.

_Assumption: You're a sysadmin or other kind of Linux expert - and we're in Ubuntu/Debian land here._

Known requires the use of a web server software that can do URL rewriting and Known recommend using Apache and mod_rewrite. Other requirements are MongoDB or MySQL and PHP 5.4 or above. I've been using Apache for so long that I'm frankly bored of it and I try and use Nginx where possible. The primary challenge then is converting the Apache URL rewriting rules provided by Known in the .htaccess document into Nginx compatible rules. In addition I found that Known needs good caching in place and I'll talk a bit about that too.

##Getting started.

I'd suggest making use of a [Vagrant](http://vagrantup.com) box and [Python Fabric](http://www.fabfile.org/) to automate some (all?) of the steps. This is good devops practice anyway and once you start doing things this way it's hard to stop. If you're looking for a virtual server at a good price give [Digital Ocean](http://digitalocean.com) a look.

For my setup I'm using Ubuntu 14.04 LTS and I'll assume you are too. I'm using mongodb as recommended by Known as there are zero extra steps required in setting up your backend DB, and I'll be using Nginx with php-fpm.

First install the following packages:

* mongodb
* nginx
* php5
* php-pear
* php5-dev
* php5-gd
* php5-curl
* php5-fpm
* php5-xmlrpc
* php5-mongo

Then check out the Known source from https://github.com/idno/idno into /var/www. Use recurssive checkout as there are submodules in the project:
```git clone --recursive https://github.com/idno/idno /var/www```

##Slight bit of code change

At this point in time (2014-08-22) there is a bit of code change to do which I've submitted to Known. By the time you read this you might not even need to bother. In the file Idno/Pages/File/View.php there is an Apache specic function call, ```$headers = apache_request_headers();```. This won't work with Ngnix so you need to apply a diff.

This should do it...

cd /var/www/idno 
curl -O https://gist.githubusercontent.com/elliottucker/ab5a8d9c12a062a839ff/raw/f86126a1d6945fa9cb5a173e8c44d4b3aa6a3b23/known_view.diff | git apply -

##Set up Known URL rewriting with Nginx

Here's part the .htaccess file provided in the Known source that we want to work on Nginx:

```
RewriteEngine on
RewriteRule ^(\.well\-known.*)$ /index.php/$1 [L]
RewriteRule ^\..* - [F]
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteCond $1 !^(index\.php)
RewriteRule ^(.*)$ /index.php/$1 [L]
```

With some mucking about I managed to translate this to Nginx rules. Include this in the Nginx "server" block config. You'll need to change server_name to the hostname or IP of your server. I've only one site on the server so I've got this in /etc/nginx/sites-available/default.

```
server {
listen 80;

root /var/www;
index index.php;

server_name example.com;
client_max_body_size 20M;

location / {
try_files $uri $uri/ /index.php?$query_string;
}

location ~ \.php$ {
fastcgi_split_path_info ^(.+\.php)(/.+)$;
fastcgi_pass unix:/var/run/php5-fpm.sock;
fastcgi_index index.php;
include fastcgi_params; 
fastcgi_param PHP_VALUE "cgi.fix_pathinfo=0 \n upload_max_filesize=1000M \n post_max_size=1080M";
}

location ~ /\.ht {
deny all;
}
location ~* \.(js|css)$ {
expires max;
log_not_found off;
}

location ~* \.(xml|ini)$ {
deny all;
}

}

I know it looks a lot bigger but note this is the config for all of the site, not just the URL rewriting part. In fact, for all intents and purposes the Apache rewriting config can be translated to just:

location / {
try_files $uri $uri/ /index.php?$query_string;
}

```
Yes, Nginx is cool, once you get your head around it.

At this point you should be good to start up Nginx and point your browser to your host or IP address...if not, sorry, this is when you need to be a sysadmin or ask on #indiewebcamp for help.

##Setting up caching with Varnish.

I noticed that none of the images stored on the DB were caching in my browser, and this was very noticible on the large background image I've set up in the theme. I might be wrong, and it could be a side effect of using Nginx, but it looks like Known is forcing no cache for all requests. Having never used Varnish before I decided that this was the man for the job, no other reason.

First of install the 'varnish' package from apt. Currently Ubuntu has Varnish 3 rather than 4 but this will do us.

Varnish will be listening on port 80 so we need to change the Nginx port to something else, e.g, 8080 and to have it only listen on locally, not on the public internet. Change the 'listen' config and then restart Nginx:

```listen 127.0.0.1:8080;```

To get Varnish to listen on port 80, change /etc/default/varnish to be the following:

```
DAEMON_OPTS="-a :80 \
-T localhost:6082 \
-f /etc/varnish/default.vcl \
-S /etc/varnish/secret \
-s malloc,256m"
START="Yes"
```

You now want to set up the rules in Varnish to know where to find the backend site you have running on Nginx port 8080. Replace /etc/varnish/default.vcl with the following.

```
backend default {
.host = "127.0.0.1";
.port = "80";
}
```

And in the same file add the following rule. Basically removing any HTTP response headers that stop caching and setting the age for all cached items to 1d for any request starting /file/.

```
sub vcl_fetch {
	if (req.url ~ "^/file/") {
		remove beresp.http.cache-control;
		set beresp.http.Cache-Control = "public, max-age=1d";
		remove beresp.http.Pragma;
		set beresp.ttl = 1d;
	}
}
```

Restart Varnish and you should be good to go to your site and start setting it up. It's worth playing with Varnish now to see if you improve caching and performance. This is something I haven't done and there's a very good chance the above config is far from optimal. Let me know your results in comments or at #indiewebcamp.

##Next Steps

Now you have your site up and running (you do don't you?) try adding some plugins. Check these out from https://github.com/idno and stick them in the IdnoPlugins directory. I think there's an issue with the Twitter plugin at the moment where I couldn't get it to save the authentication. Clear your browser session if that happens. It might help.