#!/bin/bash
MYSQL_ROOT_PASSWORD=$1
echo 'create database imovies' | mysql -uroot -p$MYSQL_ROOT_PASSWORD
mysql -uroot -p$MYSQL_ROOT_PASSWORD imovies < ../db/imovies_users.dump