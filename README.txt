Yushiroh Canastra
Sean Spearman

CS174A Final Project

/**
 * MySQL UDF
 */
We made a bash script file named script.sh to compile the UDF C file and create a .so file so we wouldn't have to keep typing the gcc commands. The same script file also moved the newly made .so file to the plugin folder for mysql so we can load the UDF functions in. Finally the script restarts the mysql server.

/**
 * Paillier Cryptography
 */
To compile the paillier program, you would just type in
	gcc mypaillier.c -o paillier -lgmp -lpallier -std=c99
This program is responsible for encryping and decrypting numbers.

The paillier library we used is from http://acsc.cs.utexas.edu/libpaillier/. We downloaded it and then ran the make file to install it. The GMP library was installed through apt-get install libgmp3-dev.

/**
 * Client
 */
To run the client compile the paillier program and put it in the same directory as cli.py then run
python cli.py
assuming Python 2.7.
You can also do the following from the client
	enc 4
or
	dec 43617959217830830880084411658637102201163120188082913598053268846623965980157
which is equivalent to
	./paillier enc 4
or
	./paillier dec 43617959217830830880084411658637102201163120188082913598053268846623965980157
respectively.