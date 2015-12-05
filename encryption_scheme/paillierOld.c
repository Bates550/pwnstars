#include <inttypes.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <gmp.h>
#include <paillier.h>

typedef struct PublicKey {
    int64_t n;
    int64_t g;
} PublicKey;

typedef struct PrivateKey {
    int64_t l;
    int64_t m;
} PrivateKey;

int getRandomInt(int min, int max);

void generateKeys(PrivateKey *priKey, PublicKey *pubKey, gmp_randstate_t rState);

int lcm(int x, int y) {
    int64_t a, b, t, gcd, lcm;
    a = x;
    b = y;

    while (b != 0) {
        t = b;
        b = a % b;
        a = t;
    }
    gcd = a;
    return x*y/gcd;
}

int isPrime(int number) {
    if (number <= 1) return 0; // zero and one are not prime
    for (int i = 2; i*i <= number; i++) {
        if (number%i == 0) return 0;
    }
    return 1;
}

int main(void) {
    srand(time(NULL));

//    for (int i = 0; i < 100; i++) {
//        generate();
//    }

    PrivateKey *a = malloc(sizeof(PrivateKey));
    PublicKey *b = malloc(sizeof(PublicKey));

    unsigned long int seed = time(NULL);

    gmp_randstate_t rState;
    gmp_randinit_default(rState);
    gmp_randseed_ui(rState, seed);

    for (int i = 0; i < 100; i++) {
        a->l = 0;
        a->m = 0;
        b->n = 0;
        b->g = 0;

        generateKeys(a, b, rState);

        printf("l: %" PRId64 " a: %" PRId64 "\n", a->l, a->m) ;//u: PRIu64, n: PRIu64, g: PRIu64\n", a->l, a->u, b->n, b->g);
    }
	return 0;
}


int getRandomInt(int min, int max) {
    double scaled = (double)rand()/RAND_MAX;
    return (int)(max - min + 1)*scaled + min;
}

int64_t power(int64_t a, int64_t b) {
    int64_t retval = 1;
    for (int64_t i = 0; i < b; i++) {
        retval *= a;
    }
    return retval;
}

void generateKeys(PrivateKey *priKey, PublicKey *pubKey, gmp_randstate_t rState) {
//    int64_t p;
//    int64_t q;
//
//    int64_t n;
//    int64_t l;
//
//    int64_t g = 1;
//    double u;
//
//    do {
//        p = getRandomInt(10, 99);
//        q = getRandomInt(10, 99);
//    } while (!isPrime(p) || !isPrime(q));
//
//    n = p*q;
//    l = lcm(p - 1, q - 1);
//
//    g = (int64_t)rand()%(n*n);
////    u = (int)(((int)pow(g, l)%(n^2) - 1)/n)%n;
////    u = 1/u;
//    printf("%" PRId64 "\n", power(g, l));
//    u = ((g*l)%(n^2) - 1)/n;
//
//    priKey->l = l;
//    priKey->u = u;
//    pubKey->n = n;
//    pubKey->g = g;



    int p;
    int q;
    mpz_t n;
    mpz_t l;
    mpz_t g;
    mpz_t m;

    mpz_t nSquared;
    mpz_t gToL;
    mpz_t u;
    mpz_t uMinus1;
    mpz_t lagRange;
    mpz_t inverse;
    mpz_t negative1;

    mpz_t temp1;
    mpz_t temp2;
    mpz_t randNum;

    mpz_init(n);
    mpz_init(l);
    mpz_init(g);
    mpz_init(m);
    mpz_init(nSquared);
    mpz_init(gToL);
    mpz_init(u);
    mpz_init(uMinus1);
    mpz_init(lagRange);
    mpz_init(inverse);
    mpz_init(negative1);
    mpz_init(temp1);
    mpz_init(temp2);
    mpz_init(randNum);

    mpz_urandomb(randNum, rState, 100);
//    gmp_printf("%Zd\n", randNum);

    mpz_set_si(negative1, -1);

    do {
        p = getRandomInt(10, 99);
        q = getRandomInt(10, 99);
//        mpz_set_si(p, getRandomInt(10, 99));
//        mpz_set_si(q, getRandomInt(10, 99));
    } while (!isPrime(p) || !isPrime(q));

    mpz_set_si(temp1, p);
    mpz_set_si(temp2, q);
    mpz_mul(n, temp1, temp2);

    mpz_set_si(l, lcm(p - 1, q - 1));

    mpz_mul(nSquared, n, n);
    mpz_mod(g, randNum, nSquared);

    mpz_pow_ui(gToL, g, mpz_get_ui(l));
    mpz_mod(u, gToL, nSquared);

    mpz_sub_ui(uMinus1, u, 1);
    mpz_div(lagRange, uMinus1, n);

    mpz_powm(m, lagRange, negative1, nSquared);

    gmp_printf("%Zd\n", m);
}
