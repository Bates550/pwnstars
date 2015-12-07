#ifdef STANDARD
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#else
#include <my_global.h>
#include <my_sys.h>

#endif
#include <mysql.h>
#include <ctype.h>
#include <gmp.h>
#include <paillier.h>

static pthread_mutex_t LOCK_hostname;

extern "C" my_bool SUM_HE_init(UDF_INIT *initid, UDF_ARGS *args, char *message);
extern "C" void SUM_HE_deinit(UDF_INIT *initid);
extern "C" char* SUM_HE(UDF_INIT *initid, UDF_ARGS *args, char *result,
                        unsigned long *length, char *is_null, char *error);
extern "C" void SUM_HE_clear(UDF_INIT *initid, char *is_null, char *error);
extern "C" void SUM_HE_add(UDF_INIT *initid, UDF_ARGS *args, char *is_null, char *error);


void setPubKey(paillier_pubkey_t *pub) {
    int bits;
    mpz_t n;
    mpz_t n_squared;
    mpz_t n_plusone;

    mpz_init(pub->n);
    mpz_init(pub->n_squared);
    mpz_init(pub->n_plusone);

    pub->bits = 128;
    mpz_set_str(pub->n, "246466378699131682045760888411731624153", 10);
    mpz_set_str(pub->n_squared, "60745675829063791326517741681938229998404992429588384339369986055667252967409", 10);
    mpz_set_str(pub->n_plusone, "246466378699131682045760888411731624154", 10);
}

my_bool SUM_HE_init(UDF_INIT *initid, UDF_ARGS *args, char *message) {
    initid->ptr = new char;
    initid->ptr[0] = '1';
    initid->ptr[1] = '\0';

	if (args->arg_count != 1) {
		strcpy(message,"SUM_HE() requires one arguments");
		return 1;
	}

	if (args->arg_type[0] != STRING_RESULT) {
		strcpy(message,"SUM_HE() requires an string");
		return 1;
	}
	return 0;
}

void SUM_HE_deinit(UDF_INIT *initid) {
	delete (char*)initid->ptr;
}

char* SUM_HE(UDF_INIT *initid, UDF_ARGS *args, char *result,
             unsigned long *length, char *is_null, char *error) {
    *length = strlen((char*)initid->ptr);
	return initid->ptr;
}

void SUM_HE_clear(UDF_INIT *initid, char *is_null, char *error) {
    initid->ptr = new char;
    initid->ptr[0] = '1';
    initid->ptr[1] = '\0';
}

void SUM_HE_add(UDF_INIT *initid, UDF_ARGS *args, char *is_null, char *error) {
    paillier_pubkey_t *pubKey = (paillier_pubkey_t*)malloc(sizeof(paillier_pubkey_t));
    setPubKey(pubKey);

    mpz_t num1;
    mpz_t num2;
    mpz_t sum;

    mpz_init(num1);
    mpz_init(num2);
    mpz_init(sum);

    mpz_set_str(num1, (char*)args->args[0], 10);
    mpz_set_str(num2, (char*)initid->ptr, 10);

    mpz_mul(sum, num1, num2);
	mpz_mod(sum, sum, pubKey->n_squared);

    initid->ptr = mpz_get_str(NULL, 10, sum);
}
