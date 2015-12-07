#!/bin/bash

gcc -shared -o MyTest.so MyTest.cc -lgmp -lpaillier -fPIC $(mysql_config --libs --cflags)
sudo mv MyTest.so /usr/lib/mysql/plugin

sudo /etc/init.d/mysql restart
