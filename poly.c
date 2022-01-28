#include <stdint.h>
#include <stdlib.h>
#include <time.h>
#include <stdio.h>
#include "params.h"
#include "reduce.h"

#if (STDDEV == 419)
static uint16_t prepared_cdf[14] = {194, 572, 920, 1220, 1466, 1656, 1794, 1890, 1952, 1990, 2012, 2024, 2030, 2032};

#elif (STDDEV == 26)
static uint16_t prepared_cdf[9] = {314, 896, 1362, 1684, 1876, 1974, 2016, 2032, 2036};

#elif (STDDEV == 3197)
static int16_t prepared_cdf[11] = {255, 741, 1161, 1489, 1721, 1871, 1957, 2003, 2025, 2033, 2035};

#elif (STDDEV == 3192)
static int16_t prepared_cdf[12] = {255, 740, 1158, 1485, 1717, 1866, 1953, 1999, 2021, 2030, 2035, 2036};

#elif (STDDEV == 319215)
static int32_t prepared_cdf[16] = {8180, 23769, 37223, 47750, 55217, 60018, 62816, 64294, 65002, 65310, 65431, 65474, 65488, 65492, 65493, 65494};

#elif (STDDEV == 319715)
static int32_t  prepared_cdf[16] = {8174, 23741, 37182, 47707, 55181, 59992, 62802, 64289, 65003, 65314, 65437, 65481, 65495, 65499, 65500, 65501};

#elif (STDDEV == 41915)
static int32_t prepared_cdf[16] = {6236, 18359, 29489, 39141, 47049, 53169, 57643, 60733, 62748, 63990, 64713, 65111, 65317, 65418, 65465, 65486};

#else
#error "STDDEV must be either 419 (4.19), 26 (2.6) or 3197 (3.197) or 319715 (3.197 for s in [0,15])"
#endif

void init_rand(int seed){
    srand(seed);
}

// uniform random integers
int randint(int n) {
  if ((n - 1) == RAND_MAX) {
    return rand();
  } else {
    int end = RAND_MAX / n;
    end *= n;
    int r;
    while ((r = rand()) >= end);
    return r % n;
  }
}

int sample_from_cdf() {
  int length = sizeof(prepared_cdf)/sizeof(prepared_cdf[0]);
  int bound = prepared_cdf[length-1];
  int r = randint(bound+1);
  if (r < prepared_cdf[0]) {
    return 0;
  }
  for (int i=0; i < length; i++) {
    if (r < prepared_cdf[i]) {
      int sign = randint(2);
      if (sign == 0){
        return i;
      } else{
        return -1 * i;
      }
    }
  }
  return 0;
}

void poly_mul_pointwise(uint32_t *r, uint32_t *a, uint32_t *b, int n)
{
  int i;
  uint16_t t;
  for(i=0;i<n;i++)
  {
    t    = montgomery_reduce(NEWHOPE_MUL*b[i]); /* t is now in Montgomery domain */
    r[i] = montgomery_reduce(a[i] * t);  /* r->coeffs[i] is back in normal domain */
  }
}

void poly_mul_int(int64_t *r, const int64_t *a, int64_t b, int n)
{
  for(int i=0;i<n;i++)
  {
    r[i] = a[i] * b;
  }
}

void poly_add(int64_t *r, const int64_t *a, const int64_t *b, int n)
{
  int i;
  for(i=0;i<n;i++){
    r[i] = a[i] + b[i];
    if (r[i] >= NEWHOPE_Q){
      r[i] = r[i] - NEWHOPE_Q;
    }
  }
}

void poly_mul(int64_t *r, int64_t *a, int64_t *b, int n)
{
  int i, j;
  for(i = 0; i < n; i++) {
    for(j = 0; j < n; j++){
      if (i + j < n){
        r[i + j] += a[i] * b[j];
        r[i + j] %= NEWHOPE_Q;
      } else {
        r[i + j - n] -= a[i] * b[j];
        r[i + j - n] %= NEWHOPE_Q;
      }
    }
  }
  for (i = 0; i < n; i++) {
    if(r[i] < 0) 
      r[i] = NEWHOPE_Q + r[i];
  }
}

void poly_mul_mont(int64_t *r, int64_t *a, int64_t *b, int n)
{
  int i,j;
  int64_t *am = malloc(sizeof(int64_t) * n);
  int64_t *bm = malloc(sizeof(int64_t) * n);
  int64_t *rm = malloc(sizeof(int64_t) * n);
  // convert a and b into Montgomery representation
  for (i = 0; i < n; i++) {
    am[i] = montgomery_reduce(NEWHOPE_MUL * a[i]);
    bm[i] = montgomery_reduce(NEWHOPE_MUL * b[i]);
    rm[i] = 0;
  }
  for (i = 0; i < n; i++) {
    for(j = 0; j < n; j++){
      if (i + j < n){
        // multiply a[i] and b[j] and add to rm[i + j]
        rm[i + j] += montgomery_reduce(am[i] * bm[j]);
        // make sure rm[i + j] doesn't get too big
        rm[i + j] = montgomery_reduce(rm[i + j]);
        rm[i + j] = montgomery_reduce(NEWHOPE_MUL * rm[i + j]);
      } else {
        // reduce mod x^n + 1
        // multiply a[i] and b[j] and subtract from rm[i + j]
        rm[i + j - n] -= montgomery_reduce(am[i] * bm[j]);
        // make sure rm[i + j] doesn't get too big
        rm[i + j - n] = montgomery_reduce(rm[i + j - n]);
        rm[i + j - n] = montgomery_reduce(NEWHOPE_MUL * rm[i + j - n]);
      }
    }
  }
  // convert result out of Montgomery representation
  for (i = 0; i < n; i++) {
    r[i] = montgomery_reduce(rm[i]);
  }
  
  // add these to free memory
  free(am);
  free(bm);
  free(rm);
}
