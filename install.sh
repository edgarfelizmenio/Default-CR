#! /bin/bash

echo "mysql-server-5.7 mysql-server/root_password password root" | sudo debconf-set-selections
echo "mysql-server-5.7 mysql-server/root_password_again password root" | sudo debconf-set-selections
sudo apt-get install -y -q mysql-server-5.7 mysql-client