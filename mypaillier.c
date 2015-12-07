#include <stdio.h>
#include <gmp.h>
#include <paillier.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>

void get_rand(void* buf, int len) {
    char *bytes = (char*)buf;
    for (int i = 0; i != len; i++) {
        bytes[i] = rand()&0xFF;
    }
}

void setKeys(paillier_pubkey_t *pub, paillier_prvkey_t *prv) {
    int bits;
    mpz_t n;
    mpz_t n_squared;
    mpz_t n_plusone;

    mpz_t lambda;
    mpz_t x;

    mpz_init(pub->n);
    mpz_init(pub->n_squared);
    mpz_init(pub->n_plusone);

    mpz_init(prv->lambda);
    mpz_init(prv->x);

    pub->bits = 128;
    mpz_set_str(pub->n, "246466378699131682045760888411731624153", 10);
    mpz_set_str(pub->n_squared, "60745675829063791326517741681938229998404992429588384339369986055667252967409", 10);
    mpz_set_str(pub->n_plusone, "246466378699131682045760888411731624154", 10);

    mpz_set_str(prv->lambda, "10269432445797153417255853088522600352", 10);
    mpz_set_str(prv->x, "238298118762531095220447747881420575017", 10);
}


int areEqual(const char *c1, const char *c2) {
    if (strlen(c1) != strlen(c2)) {
        return 0;
    }
    for (int i = 0; i < strlen(c1); i++) {
        if (c1[i] != c2[i]) {
            return 0;
        }
    }
    return 1;
}

int main(int argc, char *argv[]) {
    srand(time(NULL));

    paillier_pubkey_t *pubKey = malloc(sizeof(paillier_pubkey_t));
	paillier_prvkey_t *prvKey = malloc(sizeof(paillier_prvkey_t));

	setKeys(pubKey, prvKey);

    if (argc != 3) {
        return 1;
    }

    if (areEqual(argv[1], "enc")) {
        paillier_plaintext_t *plainText = malloc(sizeof(paillier_plaintext_t));

        paillier_plaintext_t *plainText2 = malloc(sizeof(paillier_plaintext_t));
        paillier_plaintext_t *plainText3 = malloc(sizeof(paillier_plaintext_t));
        paillier_plaintext_t *plainText4 = malloc(sizeof(paillier_plaintext_t));

        paillier_ciphertext_t  *cipherText = malloc(sizeof(paillier_ciphertext_t));

        plainText = paillier_plaintext_from_ui(atoi(argv[2]));
        paillier_enc(cipherText, pubKey, plainText, get_rand);
        gmp_printf("%Zd\n", cipherText->c);
    }
    else if (areEqual(argv[1], "dec")) {
        paillier_plaintext_t *plainText = malloc(sizeof(paillier_plaintext_t));

        paillier_ciphertext_t  *cipherText = malloc(sizeof(paillier_ciphertext_t));

        mpz_init(cipherText->c);
        mpz_set_str(cipherText->c, argv[2], 10);

        paillier_plaintext_t *plainText10 = paillier_dec(NULL, pubKey, prvKey, cipherText);
        gmp_printf("%Zd\n", plainText10->m);
    }

	return 0;
}
