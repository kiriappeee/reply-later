# Reply Later

This is a tool (still prototype) for buffering replies to tweets. To run this do the
following

##Docker Instructions##

Install Docker 

For dev I run my docker containers inside a Vagrant box that exposes port 80 on the guest
via port 8888 on the host. So if I want to go to localhost running inside the docker
container while developing, I use localhost:8888. If this matches your setting:

Run `wget https://raw.githubusercontent.com/spartakode/my-docker-repos/master/python/reply-later/dev/Dockerfile' and
`wget https://raw.githubusercontent.com/spartakode/my-docker-repos/master/python/reply-later/dev/devnginxfile'

Open up devnginxfile and change the port 8888 to whichever port you want to use

For production, the app runs on localhost (port 80). If you want to run with this setting, 

Run `wget https://raw.githubusercontent.com/spartakode/my-docker-repos/master/python/reply-later/dev/Dockerfile' and
`wget https://raw.githubusercontent.com/spartakode/my-docker-repos/master/python/reply-later/dev/devnginxfile'

Once you've done that:

Run `docker build -t replylater:app /path/to/folder/containing/Dockerfile`

clone this repo 

Copy src/sampleconfig.ini to src/config.ini and src/sampletweetconfig.ini to src/tweetconfig.ini
 
Create a Twitter app using https://apps.twitter.com/ and get your access tokens as well.
Fill in tweetconfig.ini with the relevant values.

Run `docker run -it -v /path/to/repo:/replylater -w /replylater --name replylater -p 80:80 replylater:app /bin/bash`

run python3.5 and use 

```
import os
os.geturandom(30)
```

We are using the value between the single quotes as a secret key. Open config.ini and
replace the secret key value with the one you got from os.geturandom(30)

Inside the docker machine, exit python and run the command `cron`

Then `sudo service nginx start`

Finally, `python3.5 -m serverstart.py`

Visit your browser at localhost:8888/replylater/app

And you should be up and running
