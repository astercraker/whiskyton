#!/usr/bin/env bash

# Python
apt-get update
sudo apt-get install -y python-setuptools
easy_install pip

# Node.js and CoffeeScript
apt-get install -y curl
curl -sL https://deb.nodesource.com/setup | sudo bash -
apt-get install -y nodejs
npm install -g coffee-script

# install project dependencies
pip install -r /vagrant/requirements.txt