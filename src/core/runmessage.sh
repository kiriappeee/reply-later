#!/bin/sh
replyId=$1
dataStrategy=$2

cd /replylater/
/usr/local/bin/python3.5 -m src.core.tests.CreateFile
