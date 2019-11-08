#!/bin/bash
MYSQL_ROOT_PASSWORD=$1
PATH_TO_DUMP=$2
echo 'create database imovies' | mysql -uroot -p$MYSQL_ROOT_PASSWORD
mysql -uroot -p$MYSQL_ROOT_PASSWORD imovies < $PATH_TO_DUMP