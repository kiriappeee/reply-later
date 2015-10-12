#Reply Later Experimental Branch

This readme is for the experimental branch only. To use the application please
do the following

This has been tested with python3.4 only

Make sure cron is installed and running.

Install python-crontab via pip and tweepy via the git repository using pip

Create a file called config.ini in python/ and copy the contents of
sampleconfig.ini into it

Create an app on dev.twitter.com and fill in the details. You'll need to
authenticate yourself as well to fill in dev access token and dev access secret. 

secretKey can be left as fillmein or just deleted

Navigate to the python directory. **You must do this. Do not run from outside the directory**

`python3.4 Tweet.py` and you are ready to go. You are first shown a set of
mentions that you can reply to (your latest 10). To select which tweet you want
to reply to, use the zeroth index. So for mention number 6, you need to give
the input as number 5
