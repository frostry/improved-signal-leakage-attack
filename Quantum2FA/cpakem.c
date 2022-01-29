#include <string.h>
#include "api.h"
#include "cpapke.h"
#include "params.h"
#include "randombytes.h"
#include "fips202.h"
#include "verify.h"
#include <stdio.h>
#include "poly.h"

/*************************************************
* Name:        crypto_kem_keypair
*
* Description: Generates public and private key
*              for CCA secure NewHope key encapsulation
*              mechanism
*
* Arguments:   - unsigned char *pk: pointer to output public key (an already allocated array of CRYPTO_PUBLICKEYBYTES bytes)
*              - unsigned char *sk: pointer to output private key (an already allocated array of CRYPTO_SECRETKEYBYTES bytes)
*
* Returns 0 (success)
**************************************************/
int crypto_kem_keypair(unsigned char *pk, unsigned char *sk, unsigned short int k)
{
  cpapke_keypair(pk, sk, k);                                                        /* First put the actual secret key into sk */
  // puts("cpa");
  return 0;
}

/*************************************************
* Name:        crypto_kem_enc
*
* Description: Generates cipher text and shared
*              secret for given public key
*
* Arguments:   - unsigned char *ct:       pointer to output cipher text (an already allocated array of CRYPTO_CIPHERTEXTBYTES bytes)
*              - unsigned char *ss:       pointer to output shared secret (an already allocated array of CRYPTO_BYTES bytes)
*              - const unsigned char *pk: pointer to input public key (an already allocated array of CRYPTO_PUBLICKEYBYTES bytes)
*
* Returns 0 (success)
**************************************************/
int crypto_kem_enc(unsigned char *ct, unsigned char *ss, const unsigned char *pk, poly * bobs)
{
  unsigned char buf[2*NEWHOPE_SYMBYTES];
  // for (int i = 0; i < 2*NEWHOPE_SYMBYTES; i++) {
  //   printf("%#x%c", buf[i], i + 1 == 2 * NEWHOPE_SYMBYTES ? '\n' : ' ');
  // }

  buf[0] = 0x02;
  randombytes(buf+1,NEWHOPE_SYMBYTES);
  // puts("random bytes:");
  // for (int i = 0; i < 2*NEWHOPE_SYMBYTES; i++) {
  //   printf("%#x%c", buf[i], i + 1 == 2 * NEWHOPE_SYMBYTES ? '\n' : ' ');
  // }

  shake256(buf,2*NEWHOPE_SYMBYTES,buf,NEWHOPE_SYMBYTES + 1);                     /* Don't release system RNG output */

  cpapke_enc(ct, buf, pk, buf+NEWHOPE_SYMBYTES, bobs);                                 /* coins are in buf+NEWHOPE_SYMBYTES */

  shake256(ss, NEWHOPE_SYMBYTES, buf, NEWHOPE_SYMBYTES);                         /* hash pre-k to ss */
  return 0;
}


//modified for choosing k
// int crypto_kem_enc(unsigned char *ct, unsigned char *ss, const unsigned char *pk)
// {
//   unsigned char buf[2*NEWHOPE_SYMBYTES] = {0x2, 0x4, 0xf9, 0x46, 0x1b, 0x8c, 0x1a, 0x46, 0xb2, 0x12, 0x3c, 
//                                            0x4b, 0x7c, 0x3b, 0x10, 0xcf, 0x9e, 0xdf, 0x16, 0x12, 0x90, 0xda, 
//                                            0xff, 0x6, 0xb4, 0x10, 0x28, 0xd3, 0x39, 0xd8, 0x77, 0x9c, 0xe1, 
//                                            0, 0, 0, 0, 0, 0, 0, 0xd3, 0xae, 0x6d, 0x51, 0xbd, 0x7f, 0, 0, 
//                                            0x3, 0, 0, 0, 0, 0, 0, 0, 0x20, 0xa5, 0x81, 0x51, 0xbd, 0x7f, 0, 0};

//   buf[0] = 0x02;
//   // randombytes(buf+1,NEWHOPE_SYMBYTES);

//   // puts("random bytes:");
//   // for (int i = 0; i < 2*NEWHOPE_SYMBYTES; i++) {
//   //   printf("%#x%c", buf[i], i + 1 == 2 * NEWHOPE_SYMBYTES ? '\n' : ' ');
//   // }

//   shake256(buf,2*NEWHOPE_SYMBYTES,buf,NEWHOPE_SYMBYTES + 1);                     /* Don't release system RNG output */

//   cpapke_enc(ct, buf, pk, buf+NEWHOPE_SYMBYTES);                                 /* coins are in buf+NEWHOPE_SYMBYTES */

//   shake256(ss, NEWHOPE_SYMBYTES, buf, NEWHOPE_SYMBYTES);                         /* hash pre-k to ss */
//   return 0;
// }







/*************************************************
* Name:        crypto_kem_dec
*
* Description: Generates shared secret for given
*              cipher text and private key
*
* Arguments:   - unsigned char *ss:       pointer to output shared secret (an already allocated array of CRYPTO_BYTES bytes)
*              - const unsigned char *ct: pointer to input cipher text (an already allocated array of CRYPTO_CIPHERTEXTBYTES bytes)
*              - const unsigned char *sk: pointer to input private key (an already allocated array of CRYPTO_SECRETKEYBYTES bytes)
*
* Returns 0 (success)
**************************************************/
int crypto_kem_dec(unsigned char *ss, const unsigned char *ct, const unsigned char *sk, poly * rec_bobs)
{
  cpapke_dec(ss, ct, sk, rec_bobs);

  shake256(ss, NEWHOPE_SYMBYTES, ss, NEWHOPE_SYMBYTES);                          /* hash pre-k to ss */

  return 0;
}
