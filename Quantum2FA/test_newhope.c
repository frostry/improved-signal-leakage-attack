#include "api.h"
#include "poly.h"
#include "randombytes.h"
#include <math.h>
#include <stdio.h>
#include <string.h>

#define NTESTS 1000


// int test_keys()
// {
//   unsigned char key_a[CRYPTO_BYTES], key_b[CRYPTO_BYTES];
//   unsigned char pk[CRYPTO_PUBLICKEYBYTES];
//   unsigned char sendb[CRYPTO_CIPHERTEXTBYTES];
//   unsigned char sk_a[CRYPTO_SECRETKEYBYTES];
//   int i;

//   for(i=0; i<NTESTS; i++)
//   {
//     //Alice generates a public key
//     crypto_kem_keypair(pk, sk_a);

//     //Bob derives a secret key and creates a response
//     crypto_kem_enc(sendb, key_b, pk);
  
//     //Alice uses Bobs response to get her secre key
//     crypto_kem_dec(key_a, sendb, sk_a);

//     if(memcmp(key_a, key_b, 32))
//     {
//       int j;
//       for(j=0;j<32;j++)
//         printf("%02x ", key_a[j]);
//       printf("\n");
//       for(j=0;j<32;j++)
//         printf("%02x ", key_b[j]);
//       printf("\n");
//       printf("ERROR keys\n");
//     }
//   }

//   return 0;
// }


// int test_invalid_sk_a()
// {
//   unsigned char key_a[CRYPTO_BYTES], key_b[CRYPTO_BYTES];
//   unsigned char pk[CRYPTO_PUBLICKEYBYTES];
//   unsigned char sendb[CRYPTO_CIPHERTEXTBYTES];
//   unsigned char sk_a[CRYPTO_SECRETKEYBYTES];
//   int i;

//   FILE *urandom = fopen("/dev/urandom", "r");
  
//   for(i=0; i<NTESTS; i++)
//   {
//     //Alice generates a public key
//     crypto_kem_keypair(pk, sk_a);

//     //Bob derives a secret key and creates a response
//     crypto_kem_enc(sendb, key_b, pk);

//     //Replace secret key with random values
//     fread(sk_a, CRYPTO_SECRETKEYBYTES, 1, urandom); 
  
//     //Alice uses Bobs response to get her secre key
//     crypto_kem_dec(key_a, sendb, sk_a);

//     if(!memcmp(key_a, key_b, 32))
//       printf("ERROR invalid sk_a\n");
//   }

//   fclose(urandom);

//   return 0;
// }


// int test_invalid_ciphertext()
// {
//   unsigned char key_a[CRYPTO_BYTES], key_b[CRYPTO_BYTES];
//   unsigned char pk[CRYPTO_PUBLICKEYBYTES];
//   unsigned char sendb[CRYPTO_CIPHERTEXTBYTES];
//   unsigned char sk_a[CRYPTO_SECRETKEYBYTES];
//   int i;

//   FILE *urandom = fopen("/dev/urandom", "r");
  
//   for(i=0; i<NTESTS; i++)
//   {
//     //Alice generates a public key
//     crypto_kem_keypair(pk, sk_a);

//     //Bob derives a secret key and creates a response
//     crypto_kem_enc(sendb, key_b, pk);

//     //Change some byte in the ciphertext (i.e., encapsulated key)
//     sendb[42] ^= 23;
  
//     //Alice uses Bobs response to get her secre key
//     crypto_kem_dec(key_a, sendb, sk_a);

//     if(!memcmp(key_a, key_b, 32))
//       printf("ERROR invalid sk_a\n");
//   }

//   fclose(urandom);

//   return 0;
// }

// void choose_k(void) {
//   unsigned char pk[CRYPTO_PUBLICKEYBYTES];
//   unsigned char sk[CRYPTO_SECRETKEYBYTES];

//   unsigned short int k;
  
//   unsigned char  m_enc[CRYPTO_BYTES];
//   unsigned char  m_dec[CRYPTO_BYTES];
//   unsigned char  ct[CRYPTO_CIPHERTEXTBYTES];
  
//   for (int i = 640; i < 960; i+=320) {
//     k = i;
//     crypto_kem_keypair(pk, sk, k);
//     poly s;
//     poly_frombytes(&s, sk);
//     // puts("choose k:");
//     // for(int i = 0; i < NEWHOPE_N; i++) {
//     //   printf("%d%c", s.coeffs[i] > NEWHOPE_Q/2 ?  s.coeffs[i] - NEWHOPE_Q  : s.coeffs[i],
//     //                  i + 1 == NEWHOPE_N ? '\n' : ' ');
//     // }
//     crypto_kem_enc(ct, m_enc, pk);
//     crypto_kem_dec(m_dec, ct, sk);
//   }

//   // if(!memcmp(m_enc, m_dec, 32))
//   //     printf("ERROR invalid sk_a\n");
// }
#define NOT_REC 9

void attack_test(void) {
  unsigned char pk[CRYPTO_PUBLICKEYBYTES];
  unsigned char sk[CRYPTO_SECRETKEYBYTES];

  unsigned short int k;
  
  unsigned char  m_enc[CRYPTO_BYTES];
  unsigned char  m_dec[CRYPTO_BYTES];
  unsigned char  ct[CRYPTO_CIPHERTEXTBYTES];

  // k = 880;
  k = 1260;
  poly bobs;
  poly rec_s;
  int n = 1000;
 

  int all0 = 0;
  int count = 0;
  int rec_false = 0;
   

  crypto_kem_keypair(pk, sk, k);

  for (int l = 0; l < n; l++) {
    
    crypto_kem_enc(ct, m_enc, pk, &bobs);
    
    // printf("Bob's s:\n");
    // for(int i = 0; i < NEWHOPE_N; i++) {
    //   printf("%d%c", bobs.coeffs[i] - NEWHOPE_Q, (i + 1) == NEWHOPE_N ? '\n' : ' ');
    // }
    // printf("count 0: %d %.2f%%\n", count, count / (double) NEWHOPE_N * 100 );

    for(int i = 0; i < NEWHOPE_N; i++) {
      rec_s.coeffs[i] = NOT_REC;
    }

    crypto_kem_dec(m_dec, ct, sk, &rec_s);

    // printf("Recover s:\n");
    // for(int i = 0; i < NEWHOPE_N; i++) {
    //   if (rec_s.coeffs[i] == NOT_REC) 
    //     printf("%d%c", 9, (i + 1) == NEWHOPE_N ? '\n' : ' ');
    //   else
    //     printf("%d%c", rec_s.coeffs[i] - NEWHOPE_Q, (i + 1) == NEWHOPE_N ? '\n' : ' ');
    // }

    if (k == 880) {
      for(int i = 0; i < NEWHOPE_N; i++) {
        if ( bobs.coeffs[i] == NEWHOPE_Q ) 
            all0++;
        if ( rec_s.coeffs[i] == (0 + NEWHOPE_Q) ) {
          if ( bobs.coeffs[i] == NEWHOPE_Q ) {
            count++;
          }
          else if ( bobs.coeffs[i] == NEWHOPE_Q - 7 ||  bobs.coeffs[i] == NEWHOPE_Q + 7) {
            rec_false++;
            // printf("%d\n", bobs.coeffs[i] - NEWHOPE_Q);
          }
          else {
            printf("Strange case s[i] = %d \n", bobs.coeffs[i] - NEWHOPE_Q);
          }
        }
      }
    }
    else {
      for(int i = 0; i < NEWHOPE_N; i++) {
        if ( bobs.coeffs[i] == NEWHOPE_Q || bobs.coeffs[i] == NEWHOPE_Q-1 || bobs.coeffs[i] == NEWHOPE_Q+1) 
            all0++;
        if ( rec_s.coeffs[i] != NOT_REC ) {
            count++;
            if ( rec_s.coeffs[i] != bobs.coeffs[i] )
              rec_false++;
        }
      }
    }
  }

  if (k == 880) {
    printf("all 0: %d\n", all0);
    printf("all correctly recovered: %d %.2f%%\n", count, count / (float) all0 * 100 );
    printf("recovery failed: %d\n", rec_false);
    
    printf("average recovery: %.2f%% %.2f%%\n", (count + rec_false)  / (float)(NEWHOPE_N * n) * 100, 
                                                count / (float)(NEWHOPE_N * n) * 100);
    printf("correct rate: %.2f%%\n", count / (float)(count + rec_false) * 100);
  }
  else {
    printf("all 0,1,-1: %d\n", all0);
    printf("all recovered: %d %.2f%%\n", count, (count - rec_false) / (float) all0 * 100);
    printf("recovery failed: %d\n", rec_false);
    printf("average recovery: %.2f%% %.2f%%\n", count  / (float)(NEWHOPE_N * n) * 100, 
                                                (count - rec_false) / (float)(NEWHOPE_N * n) * 100);
    printf("correct rate: %.2f%%\n", (count - rec_false) / (float)count * 100);
  }

}


int main(void){

  // test_keys();
  /*
  test_invalid_sk_a();
  test_invalid_ciphertext();
  */
  
  // printf("CRYPTO_SECRETKEYBYTES:  %d\n",CRYPTO_SECRETKEYBYTES);
  // printf("CRYPTO_PUBLICKEYBYTES:  %d\n",CRYPTO_PUBLICKEYBYTES);
  // printf("CRYPTO_CIPHERTEXTBYTES: %d\n",CRYPTO_CIPHERTEXTBYTES);


  /* Attack */
  // choose_k();
  attack_test();


  return 0;
}
