#include <stdio.h>
#include "api.h"
#include "poly.h"
#include "randombytes.h"
#include "fips202.h"

/*************************************************
* Name:        encode_pk
* 
* Description: Serialize the public key as concatenation of the
*              serialization of the polynomial pk and the public seed
*              used to generete the polynomial a.
*
* Arguments:   unsigned char *r:          pointer to the output serialized public key
*              const poly *pk:            pointer to the input public-key polynomial
*              const unsigned char *seed: pointer to the input public seed
**************************************************/
static void encode_pk(unsigned char *r, const poly *pk, const unsigned char *seed)
{
  int i;
  poly_tobytes(r, pk);
  for(i=0;i<NEWHOPE_SYMBYTES;i++)
    r[NEWHOPE_POLYBYTES+i] = seed[i];
}

/*************************************************
* Name:        decode_pk
* 
* Description: De-serialize the public key; inverse of encode_pk
*
* Arguments:   poly *pk:               pointer to output public-key polynomial
*              unsigned char *seed:    pointer to output public seed
*              const unsigned char *r: pointer to input byte array
**************************************************/
static void decode_pk(poly *pk, unsigned char *seed, const unsigned char *r)
{
  int i;
  poly_frombytes(pk, r);
  for(i=0;i<NEWHOPE_SYMBYTES;i++)
    seed[i] = r[NEWHOPE_POLYBYTES+i];
}

/*************************************************
* Name:        encode_c
* 
* Description: Serialize the ciphertext as concatenation of the
*              serialization of the polynomial b and serialization
*              of the compressed polynomial v
*
* Arguments:   - unsigned char *r: pointer to the output serialized ciphertext
*              - const poly *b:    pointer to the input polynomial b
*              - const poly *v:    pointer to the input polynomial v
**************************************************/
static void encode_c(unsigned char *r, const poly *b, const poly *v)
{
  poly_tobytes(r,b);
  poly_compress(r+NEWHOPE_POLYBYTES,v);
}

/*************************************************
* Name:        decode_c
* 
* Description: de-serialize the ciphertext; inverse of encode_c
*
* Arguments:   - poly *b:                pointer to output polynomial b
*              - poly *v:                pointer to output polynomial v
*              - const unsigned char *r: pointer to input byte array
**************************************************/
static void decode_c(poly *b, poly *v, const unsigned char *r)
{
  poly_frombytes(b, r);
  poly_decompress(v, r+NEWHOPE_POLYBYTES);
}

/*************************************************
* Name:        gen_a
* 
* Description: Deterministically generate public polynomial a from seed
*
* Arguments:   - poly *a:                   pointer to output polynomial a
*              - const unsigned char *seed: pointer to input seed
**************************************************/
static void gen_a(poly *a, const unsigned char *seed)
{
  poly_uniform(a,seed);
}


/*************************************************
* Name:        cpapke_keypair
* 
* Description: Generates public and private key 
*              for the CPA public-key encryption scheme underlying
*              the NewHope KEMs
*
* Arguments:   - unsigned char *pk: pointer to output public key
*              - unsigned char *sk: pointer to output private key
**************************************************/
void cpapke_keypair(unsigned char *pk,
                    unsigned char *sk, unsigned short int k)
{
  poly ahat, ehat, ahat_shat, bhat, shat;
  unsigned char z[2*NEWHOPE_SYMBYTES];
  unsigned char *publicseed = z;
  unsigned char *noiseseed = z+NEWHOPE_SYMBYTES;

  z[0] = 0x01;
  randombytes(z+1, NEWHOPE_SYMBYTES);
  shake256(z, 2*NEWHOPE_SYMBYTES, z, NEWHOPE_SYMBYTES + 1);

  gen_a(&ahat, publicseed);

  poly_sample(&shat, noiseseed, 0);

  //set s = 0
  // for(int i = 0; i < NEWHOPE_N; i++) {
  //   shat.coeffs[i] = 0 + NEWHOPE_Q;
  // }
  // puts("Alice's s:");
  // for(int i = 0; i < NEWHOPE_N; i++) {
  //   printf("%d%c", shat.coeffs[i] - NEWHOPE_Q, (i + 1) == NEWHOPE_N ? '\n' : ' ');
  // }

  poly_tobytes(sk, &shat);
  

  poly_ntt(&shat);

  poly_sample(&ehat, noiseseed, 1);
  
  //set e = k
  // puts("errors:");
  // // unsigned short int k = 1;
  // for(int i = 0; i < NEWHOPE_N; i++) {
  //   if (i == 0) {
  //     ehat.coeffs[i] = k + NEWHOPE_Q;
  //   }
  //   else {
  //     ehat.coeffs[i] = 0 + NEWHOPE_Q;
  //   }
  // }
  // for(int i = 0; i < NEWHOPE_N; i++) {
  //   printf("%d%c", ehat.coeffs[i] - NEWHOPE_Q, (i + 1) == NEWHOPE_N ? '\n' : ' ');
  // }
  // puts("");

  poly_ntt(&ehat);

  // for(int i = 0; i < NEWHOPE_N; i++) {
  //   printf("%d%c", ehat.coeffs[i], (i + 1) == NEWHOPE_N ? '\n' : ' ');
  // }
  // puts("");

  // poly_mul_pointwise(&ahat_shat, &shat, &ahat);
  // poly_add(&bhat, &ehat, &ahat_shat);
  
  for(int i = 0; i < NEWHOPE_N; i++) {
    if (i == 0) {
      bhat.coeffs[i] = k + NEWHOPE_Q;
    }
    else {
      bhat.coeffs[i] = 0;
    }
  }

  // printf("bhat: %d\n", bhat.coeffs[0] - NEWHOPE_Q);
  // puts("bhat:");
  // for(int i = 0; i < NEWHOPE_N; i++) {
  //   printf("%d%c", bhat.coeffs[i], (i + 1) == NEWHOPE_N ? '\n' : ' ');
  // }
  
  
  poly_ntt(&bhat);

  // poly_tobytes(sk, &shat);

  encode_pk(pk, &bhat, publicseed);
}

#if (NEWHOPE_N == 512)
static uint16_t rec_index[] = {
  0,256,128,384,64,320,192,448,32,288,160,416,96,352,224,480,16,272,144,400,80,336,208,464,48,304,176,432,112,368,240,496,8,
  264,136,392,72,328,200,456,40,296,168,424,104,360,232,488,24,280,152,408,88,344,216,472,56,312,184,440,120,376,248,504,4,
  260,132,388,68,324,196,452,36,292,164,420,100,356,228,484,20,276,148,404,84,340,212,468,52,308,180,436,116,372,244,500,12,
  268,140,396,76,332,204,460,44,300,172,428,108,364,236,492,28,284,156,412,92,348,220,476,60,316,188,444,124,380,252,508,2,
  258,130,386,66,322,194,450,34,290,162,418,98,354,226,482,18,274,146,402,82,338,210,466,50,306,178,434,114,370,242,498,10,
  266,138,394,74,330,202,458,42,298,170,426,106,362,234,490,26,282,154,410,90,346,218,474,58,314,186,442,122,378,250,506,6,
  262,134,390,70,326,198,454,38,294,166,422,102,358,230,486,22,278,150,406,86,342,214,470,54,310,182,438,118,374,246,502,14,
  270,142,398,78,334,206,462,46,302,174,430,110,366,238,494,30,286,158,414,94,350,222,478,62,318,190,446,126,382,254,510,1,
  257,129,385,65,321,193,449,33,289,161,417,97,353,225,481,17,273,145,401,81,337,209,465,49,305,177,433,113,369,241,497,9,
  265,137,393,73,329,201,457,41,297,169,425,105,361,233,489,25,281,153,409,89,345,217,473,57,313,185,441,121,377,249,505,5,
  261,133,389,69,325,197,453,37,293,165,421,101,357,229,485,21,277,149,405,85,341,213,469,53,309,181,437,117,373,245,501,13,
  269,141,397,77,333,205,461,45,301,173,429,109,365,237,493,29,285,157,413,93,349,221,477,61,317,189,445,125,381,253,509,3,
  259,131,387,67,323,195,451,35,291,163,419,99,355,227,483,19,275,147,403,83,339,211,467,51,307,179,435,115,371,243,499,11,
  267,139,395,75,331,203,459,43,299,171,427,107,363,235,491,27,283,155,411,91,347,219,475,59,315,187,443,123,379,251,507,7,
  263,135,391,71,327,199,455,39,295,167,423,103,359,231,487,23,279,151,407,87,343,215,471,55,311,183,439,119,375,247,503,15,
  271,143,399,79,335,207,463,47,303,175,431,111,367,239,495,31,287,159,415,95,351,223,479,63,319,191,447,127,383,255,511
};
#elif (NEWHOPE_N == 1024)
static uint16_t rec_index[] = { 0,512,256,768,128,640,384,896,64,576,320,832,192,704,448,960,32,544,288,800, };

#endif

/*************************************************
* Name:        cpapke_enc
* 
* Description: Encryption function of
*              the CPA public-key encryption scheme underlying
*              the NewHope KEMs
*
* Arguments:   - unsigned char *c:          pointer to output ciphertext
*              - const unsigned char *m:    pointer to input message (of length NEWHOPE_SYMBYTES bytes)
*              - const unsigned char *pk:   pointer to input public key
*              - const unsigned char *coin: pointer to input random coins used as seed
*                                           to deterministically generate all randomness
**************************************************/
void cpapke_enc(unsigned char *c,
                const unsigned char *m,
                const unsigned char *pk,
                const unsigned char *coin,
                poly * bobs)
{
  poly sprime, eprime, vprime, ahat, bhat, eprimeprime, uhat, v;
  unsigned char publicseed[NEWHOPE_SYMBYTES];

  poly_frommsg(&v, m);


  //set m = 0
  // for(int i = 0; i < NEWHOPE_N; i++) {
  //   v.coeffs[i] = 0;
  //   // v.coeffs[i] = 6144;
  //   // printf("%d%c", v.coeffs[i], (i + 1) == NEWHOPE_N ? '\n' : ' ');
  // }
  // puts("Bob's m:");
  // for(int i = 0; i < NEWHOPE_N; i++) {
  //   printf("%d%c", v.coeffs[i], (i + 1) == NEWHOPE_N ? '\n' : ' ');
  // }

  decode_pk(&bhat, publicseed, pk);

  // puts("Bob decodes pk:");
  // for(int i = 0; i < NEWHOPE_N; i++) {
  //   printf("%d%c", bhat.coeffs[i], (i + 1) == NEWHOPE_N ? '\n' : ' ');
  // }

  gen_a(&ahat, publicseed);

  poly_sample(&sprime, coin, 0);
  


  // for (int i = 0; i < NEWHOPE_N; i++) {
  //   // printf("%d\n", (NEWHOPE_Q + i)  < NEWHOPE_Q ? (NEWHOPE_Q + i) : i);
  //   sprime.coeffs[i] = NEWHOPE_Q + 0;
  // }

  // sprime.coeffs[0] = -1 + NEWHOPE_Q;
  // for (int i = -8; i <= 8; i++) {
  //   // printf("%d\n", (NEWHOPE_Q + i)  < NEWHOPE_Q ? (NEWHOPE_Q + i) : i);
  //   sprime.coeffs[i + 8] = NEWHOPE_Q + i;
  // }


  for(int i = 0; i < NEWHOPE_N; i++) {
    bobs->coeffs[i] =  sprime.coeffs[i];
  }

  poly_sample(&eprime, coin, 1);
  poly_sample(&eprimeprime, coin, 2);

  // printf("Bob's epp: %d\n", eprimeprime.coeffs[0] - NEWHOPE_Q);
  // for(int i = 0; i < NEWHOPE_N; i++) {
  //     // eprimeprime.coeffs[i] = 8;
  //   // else {
  //     // eprimeprime.coeffs[i] = NEWHOPE_Q - 8;
  //   // }
  //   // printf("%d%c", eprimeprime.coeffs[i] - NEWHOPE_Q, (i + 1) == NEWHOPE_N ? '\n' : ' ');
  // }

  poly_ntt(&sprime);
  poly_ntt(&eprime);

  poly_mul_pointwise(&uhat, &ahat, &sprime);
  poly_add(&uhat, &uhat, &eprime);

  poly_mul_pointwise(&vprime, &bhat, &sprime);
  poly_invntt(&vprime);

//   printf("Bob computes pk*s:\n");

// #define ABS(x) ( (x) < 0 ? -(x) : (x) )

//   for (int i = 0; i < 17; i++) {
//     int temp = vprime.coeffs[rec_index[i]];
//     printf("%d ", ABS(temp - 0) < ABS(temp - NEWHOPE_Q) 
//                   ? temp 
//                   : (temp - NEWHOPE_Q) % NEWHOPE_Q);
//     // printf("%d ", (vprime.coeffs[rec_index[i]] - NEWHOPE_Q) % NEWHOPE_Q);
//   }
//   printf("\n");
  // printf("%d\n", vprime.coeffs[0]);
  // for(int i = 0; i < NEWHOPE_N; i++) {
  //   printf("%d%c", (vprime.coeffs[i] - NEWHOPE_Q) % NEWHOPE_Q, (i + 1) == NEWHOPE_N ? '\n' : ' ');
  // }
  // for(int i = 0; i < NEWHOPE_N; i++) {
  //   printf("%d%c", vprime.coeffs[i], (i + 1) == NEWHOPE_N ? '\n' : ' ');
  // }

  poly_add(&vprime, &vprime, &eprimeprime);
  poly_add(&vprime, &vprime, &v); // add message

  // puts("Bob computes c:");
  // for(int i = 0; i < 17; i++) {
  //   printf("%d%c", vprime.coeffs[rec_index[i]], (i + 1) == 17 ? '\n' : ' ');
  // }

  encode_c(c, &uhat, &vprime);
}



/*************************************************
* Name:        cpapke_dec
* 
* Description: Decryption function of
*              the CPA public-key encryption scheme underlying
*              the NewHope KEMs
*
* Arguments:   - unsigned char *m:        pointer to output decrypted message
*              - const unsigned char *c:  pointer to input ciphertext
*              - const unsigned char *sk: pointer to input secret key
**************************************************/
void cpapke_dec(unsigned char *m,
                const unsigned char *c,
                const unsigned char *sk, poly * rec_bobs)
{
  poly vprime, uhat, tmp, shat;

  poly_frombytes(&shat, sk);

  decode_c(&uhat, &vprime, c);

  // printf("Alice decodes v:\n");
  // for(int i = 0; i < 17; i++) {
  //   printf("%d%c", vprime.coeffs[rec_index[i]], (i + 1) == NEWHOPE_N ? '\n' : ' ');
  //   // printf("%f%c", vprime.coeffs[rec_index[i]] / (float)NEWHOPE_Q, (i + 1) == NEWHOPE_N ? '\n' : ' ');
  // }
  // printf("\n\n");

  /* k = 880 */
  // for(int i = 0; i < NEWHOPE_N; i++) {
  //   if ( vprime.coeffs[rec_index[i]] == 0 || vprime.coeffs[rec_index[i]] == 6145 ) {
  //     rec_bobs->coeffs[i] = 0 + NEWHOPE_Q;
  //   }
  // }

  // k = 1260 
  for(int i = 0; i < NEWHOPE_N; i++) {
    if ( vprime.coeffs[rec_index[i]] == 0 || vprime.coeffs[rec_index[i]] == 6145 ) {
      rec_bobs->coeffs[i] = NEWHOPE_Q + 0;
    }
    if ( vprime.coeffs[rec_index[i]] == 4608 || vprime.coeffs[rec_index[i]] == 10753 ) {
      rec_bobs->coeffs[i] = NEWHOPE_Q - 1;
    }
    if ( vprime.coeffs[rec_index[i]] == 1536 || vprime.coeffs[rec_index[i]] == 7681 ) {
      rec_bobs->coeffs[i] = NEWHOPE_Q + 1;
    }
  }

  poly_mul_pointwise(&tmp, &shat, &uhat);
  poly_invntt(&tmp);

  poly_sub(&tmp, &tmp, &vprime);

  poly_tomsg(m, &tmp);
}
