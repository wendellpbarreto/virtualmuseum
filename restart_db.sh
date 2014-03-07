#!/bin/bash
#
#-----------------------------------
# @autor: Wendell P. Barreto
# @email: wendellp.barreto@gmail.com
# @project: virtualmuseum
# @doc: restart_db.sh
# ----------------------------------


while true; do
    read -p "Are you using Linux (y or n)? " yn
    case $yn in
        [Yy]* )
        	sudo -u postgres psql -c 'DROP DATABASE virtualmuseum_db'
			sudo -u postgres psql -c 'CREATE DATABASE virtualmuseum_db'
			sudo -u postgres psql -c 'CREATE USER virtualmuseum_admin'
			sudo -u postgres psql -c "ALTER USER virtualmuseum_admin WITH PASSWORD 'q1IUilS14,747Qx'"
			sudo -u postgres psql -c 'GRANT ALL PRIVILEGES ON DATABASE virtualmuseum_db TO virtualmuseum_admin'
			sudo -u postgres psql -d virtualmuseum_db -c 'CREATE EXTENSION hstore' 

			break;;
        [Nn]* ) 
			psql -c 'DROP DATABASE virtualmuseum_db'
			psql -c 'CREATE DATABASE virtualmuseum_db'
			psql -c 'CREATE USER virtualmuseum_admin'
			sudo -u postgres psql -c "ALTER USER virtualmuseum_admin WITH PASSWORD 'q1IUilS14,747Qx'"
			psql -c 'GRANT ALL PRIVILEGES ON DATABASE virtualmuseum_db TO virtualmuseum_admin'
			psql -d virtualmuseum_db -c 'CREATE EXTENSION hstore'

			break;;
        * ) echo "Please answer yes or no.";;
    esac
done

python manage.py syncdb
python manage.py collectstatic