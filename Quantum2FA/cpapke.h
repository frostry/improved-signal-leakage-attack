#ifndef INDCPA_H
#define INDCPA_H

#include "poly.h"

void cpapke_keypair(unsigned char *pk, 
                    unsigned char *sk,
                    unsigned short int k);

void cpapke_enc(unsigned char *c,
               const unsigned char *m,
               const unsigned char *pk,
               const unsigned char *coins,
               poly *bobs);

void cpapke_dec(unsigned char *m,
               const unsigned char *c,
               const unsigned char *sk,
               poly * rec_bobs);

#endif
