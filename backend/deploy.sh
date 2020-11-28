#!/bin/bash

cd daemons/git-webhook
ps -ef | grep -v grep | grep gw_daemon.py | awk {'print $2'} | xargs kill -9
nohup python3 gw_daemon.py > logs/nohup.out 2>&1 &

cd ../..
docker-compose up --build -d --remove-orphans
