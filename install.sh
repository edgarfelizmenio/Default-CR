#! /bin/bash -x

# Installation file of the client registry. Run ./install.sh to install.

apt-get -y -q update
apt-get -y -q upgrade
apt-get -y -q install htop
apt-get -y -q install build-essential
apt-get -y -q install git
apt-get -y -q install vim

apt-get -y -q install python python-dev
apt-get -y -q install python-pip

apt-get -y -q install libssl-dev libffi-dev python3-dev
apt-get -y -q install python3-pip
apt-get -y -q install python3.4-venv

apt-get -y -q install nginx

debconf-set-selections <<< 'mysql-server-5.6 mysql-server/root_password password password'
debconf-set-selections <<< 'mysql-server-5.6 mysql-server/root_password_again password password'
apt-get -y -q install mysql-server-5.6 mysql-client-5.6

mysql --user=root --password=password --execute="CREATE DATABASE raw_cr"
mysql --user=root --password=password raw_cr --execute="raw_cr.sql"

pyvenv-3.4 env
source env/bin/activate
pip3 install --upgrade pip

pip3 install -r requirements.txt

# install gunicorn
pip3 install gunicorn

# install and enable nginx
cp nginx/default-cr-nginx /etc/nginx/sites-available/default-cr-nginx
ln -s /etc/nginx/sites-available/default-cr-nginx /etc/nginx/sites-enabled/default-cr-nginx
sudo service nginx restart

# start the mediator
cp upstart/default-cr-upstart.conf /etc/init/default-cr.conf
sudo service default-cr start