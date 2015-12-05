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

	paillier_pubkey_t *pubKey; // = malloc(sizeof(paillier_pubkey_t));
	paillier_prvkey_t *prvKey; // = malloc(sizeof(paillier_prvkey_t));

    paillier_plaintext_t  *p1 = malloc(sizeof(paillier_plaintext_t));
//    paillier_plaintext_t  *p2 = malloc(sizeof(paillier_plaintext_t));
    paillier_ciphertext_t *c1 = malloc(sizeof(paillier_ciphertext_t));
    paillier_ciphertext_t *c2 = malloc(sizeof(paillier_ciphertext_t));

    paillier_plaintext_t  *productP = malloc(sizeof(paillier_plaintext_t));
    paillier_ciphertext_t *productC = malloc(sizeof(paillier_ciphertext_t));

    p1 = paillier_plaintext_from_ui(rand()%100);
//    p2 = paillier_plaintext_from_ui(rand()%100);

	paillier_keygen(128, &pubKey, &prvKey, get_rand);

	paillier_enc(c1, pubKey, p1, get_rand);
//	paillier_enc(c2, pubKey, p2, get_rand);

//    paillier_mul(pubKey, productC, c1, c2);

	paillier_dec(productP, pubKey, prvKey, c1);

//	gmp_printf("%Zd + %Zd = %Zd\n", p1->m, p2->m, productP->m);

//	gmp_printf("\nPublic Key\nbits: %d\nn:%Zd\nn_squared: %Zd\nn_plusone: %Zd\n",
//               pubKey->bits, pubKey->n, pubKey->n_squared, pubKey->n_plusone);
//
//    gmp_printf("\nPrivate Key\nlambda: %Zd\nx: %Zd\n", prvKey->lambda, prvKey->x);

	return 0;
}
