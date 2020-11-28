docker-compose down --remove-orphans --rmi all
docker-compose rm --stop --force
sh daemons/kill_daemons.sh
rm daemons/git-webhook/logs/*