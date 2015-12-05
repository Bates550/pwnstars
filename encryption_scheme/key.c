#include <stdio.h>
#include <gmp.h>
#include <paillier.h>
#include <stdlib.h>
#include <time.h>

void get_rand(void* buf, int len) {
    char *bytes = (char*)buf;
    for (int i = 0; i != len; i++) {
        bytes[i] = rand()&0xFF;
    }
}

int main(void) {
    srand(time(NULL));

	paillier_pubkey_t *pubKey;
	paillier_prvkey_t *prvKey;

	paillier_keygen(128, &pubKey, &prvKey, get_rand);

    gmp_printf("\nPublic Key\nbits: %d\nn:%Zd\nn_squared: %Zd\nn_plusone: %Zd\n",
               pubKey->bits, pubKey->n, pubKey->n_squared, pubKey->n_plusone);

    gmp_printf("\nPrivate Key\nlambda: %Zd\nx: %Zd\n\n", prvKey->lambda, prvKey->x);

	return 0;
}
