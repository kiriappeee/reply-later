# Reply Later

This is a tool (still prototype) for buffering replies to tweets. To run this do the
following

## Docker Instructions ##

Install Docker

For dev I run my docker containers inside a Vagrant box that exposes port 80 on the guest
via port 8888 on the host. So if I want to go to localhost running inside the docker
container while developing, I use localhost:8888. If this matches your setting:

Run `docker pull spartakode/reply-later:dev`

You can modify the port later by going into the docker container, going to
/etc/nginx/sites-available and modifying the content

If you are running on the standard port 80,

Run `docker pull spartakode/reply-later:production`

Run `docker tag spartakode/replaylater:<tag-you-pulled> replylater:app`

Run `docker run -it -v /path/to/repo:/replylater -w /replylater --name replylater -p 80:80 replylater:app /bin/bash`

Then `sudo service nginx start`

## Non docker instructions ##

For this you'll need to install python3.5 (it should work on python3+ but I haven't tested so no guarantees)

Then run `pip3.5 install requirements.txt`

## Common instructions ##

Run the command `cron`

Copy src/sampleconfig.ini to src/config.ini and src/sampletweetconfig.ini to src/tweetconfig.ini

Create a Twitter app using https://apps.twitter.com/ and get your access tokens as well.
Fill in tweetconfig.ini with the relevant values.

Run python3.5 and use

```
import os
os.geturandom(30)
```

We are using the value between the single quotes as a secret key. Open config.ini and
replace the secret key value with the one you got from os.geturandom(30)

Finally, `python3.5 -m serverstart.py`

Visit your browser at localhost:<port-of-your-choice>/replylater/app

And you should be up and running
