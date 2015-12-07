Yushiroh Canastra 
Sean Spearman

CS174A Final Project

We made a bash script file named script.sh to compile the UDF C file and create a .so file so we wouldn't have to keep typing the gcc commands. The same script file also moved the newly made .so file to the plugin folder for mysql so we can load the UDF functions in. Finally the script restarts the mysql server.

To compile the pallier program, you would just type in
gcc mypaillier.c -o paillier -lgmp -lpallier -std=c99
This program is responsible for encryping and decryping numbers.  

The paillier library we used is from http://acsc.cs.utexas.edu/libpaillier/. We downloaded it and then ran the make file to install it. The GMP library was installed through apt-get install libgmp3-dev.


