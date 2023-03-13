import math
from gpoly import *
import random
import helper
from ctypes import *
import cProfile
import time
from itertools import count, repeat, tee
from multiprocessing import Pool
from sys import exit, argv

class Ding19(object):
    def __init__(self, n, q, sigma, seed):
        self.n = n
        self.q = q
        self.sigma = sigma
        self.a = Poly.uniform(self.n, self.q)
        self.si = Ding19.gen_secret(self.n, self.q, self.sigma)
        self.ei = Ding19.gen_pubkey_error(self.n, self.q, self.sigma)
        self.sj = Ding19.gen_secret(self.n, self.q, self.sigma, seed)
        self.ej = Ding19.gen_pubkey_error(self.n, self.q, self.sigma, seed)

    @staticmethod
    def gen_secret(n, q, sigma, seed = None):
        return Poly.discretegaussian(n, q, sigma, seed)

    @staticmethod
    def gen_pubkey_error(n, q, sigma, seed = None):
        return Poly.discretegaussian(n, q, sigma)

    @staticmethod
    def gen_shared_error(n, q, sigma):
        return Poly.discretegaussian(n, q, sigma)

    @staticmethod
    def sig(q, v):
        # v = v % q
        if v > round(q / 4.0) and v < q - math.floor(q / 4):
            return 1
        else:
            return 0

    def signal(self, v):
        return [Ding19.sig(self.q, v[i]) for i in range(self.n)]

    def mod2(self, v, w):
        if self.n != v.n or self.n != len(w): raise Exception
        r = [0 for i in range(self.n)]
        for i in range(self.n):
            r[i] = int(v[i] + w[i] * (self.q - 1) / 2)
            r[i] %= self.q
            r[i] %= 2
        return r
        
    def hash1(self, Pi, Pj, xi):
        seed = hash(str(Pi) + str(Pj) + str(xi))
        return Poly.discretegaussian(self.n, self.q, self.sigma, seed)
        
    def hash2(self, Pi, Pj, xi, yj):
        seed = hash(str(Pi) + str(Pj) + str(xi) + str(yj))
        return Poly.discretegaussian(self.n, self.q, self.sigma, seed)

    def alice_init(self):
        self.xi = self.a * self.si + 2 * self.ei
        return self.xi

    def bob(self, Pi, Pj, xi, simplified=False):
        self.yj = self.a * self.sj + 2 * self.ej
        c = self.hash1(Pi, Pj, xi)
        d = self.hash2(Pi, Pj, xi, self.yj)
        if simplified:
            self.fj = Poly(self.n,self.q)
            self.gj = Poly(self.n,self.q)
        else:
            self.fj = Ding19.gen_shared_error(self.n, self.q, self.sigma)
            self.gj = Ding19.gen_shared_error(self.n, self.q, self.sigma)
        xibar = xi + self.a * c + 2 * self.fj
        self.kj = xibar * (self.sj + d) + 2 * self.gj
        
        # Error = 2*self.fj*self.sj + 2*self.fj*d + 2*self.gj + (-2)*c*self.ej
        # if max(Error) > 2000:
        #     print(max(Error))
        
        if simplified:
            self.kj += 2 * c * self.ej
        self.wj = self.signal(self.kj)
        self.skj = self.mod2(self.kj, self.wj)
        return (self.yj, self.wj, self.skj)
    
    def alice_resp(self, Pi, Pj, yj, wj):
        c = self.hash1(Pi, Pj, self.xi)
        d = self.hash2(Pi, Pj, self.xi, yj)
        self.fi = Ding19.gen_shared_error(self.n, self.q, self.sigma)
        yjbar = yj + self.a * d + 2 * self.fi
        self.gi = Ding19.gen_shared_error(self.n, self.q, self.sigma)
        self.ki = yjbar * (self.si + c) + 2 * self.gi
        self.ski = self.mod2(self.ki, wj)
        return self.ski

def get_zeros(coeffs, n):
    zero_count = 0
    temp_count = 0
    for i in range(n):
        if coeffs[i] == 0:
            temp_count += 1
        else:
            if temp_count > zero_count:
                zero_count = temp_count
            temp_count = 0
    return zero_count

def getsig(k, n, q, kn_bnd):
    global execution
    global f
    Pj = "Bob"
    Pi = 0
    signals = [None for i in range(n)]
    a = execution.a

    pa = k * f
    # print(pa)
    got_signals = 0
    query = 0
    while got_signals < n:
        Pi = Pi + 1
        (yj, wj, skj) = execution.bob(Pi, Pj, pa, False)
        query += 1
        c = execution.hash1(Pi, Pj, pa)
        d = execution.hash2(Pi, Pj, pa, yj)
        known = c * yj + a * c * d + d * pa
        for i in range(n):
            # if abs(known[i]) <= kn_bnd and signals[i] == None:
            if (known[i] <= kn_bnd or known[i] >= (q - kn_bnd)) and signals[i] == None:
                signals[i] = wj[i]
                got_signals += 1
        # print(got_signals)
    return signals, query

def sign_sBp(n, q, sB, sBp, *para):
    global execution
    global f

    Pj = "Bob"
    Pi = 0
    signals = [None for i in range(n)]
    a = execution.a

    k = para[0]
    bndh = para[1]
    bndl = para[2]

    pa = k * f
    got_signals = 0
    query = 0

    while got_signals < n:
        Pi = Pi + 1
        (yj, wj, skj) = execution.bob(Pi, Pj, pa, False)
        query += 1
        c = execution.hash1(Pi, Pj, pa)
        d = execution.hash2(Pi, Pj, pa, yj)
        known = c * yj + a * c * d + d * pa
        for i in range(n):
            if bndl <= known[i] <= bndh and signals[i] == None:
                signals[i] = wj[i]
                got_signals += 1
    # print("query: ", query)
    # print(signals)
    for i in range(n):
        if signals[i] == 0:
            sBp[i] = -sBp[i]    
    return [sBp, query]

def improvesla(n, q, sB, wk):
    global f
    f[0] = 1
    
    allk1 = [
        [75200, 150300, 526400, int(q/2)],
        [306900, 613700, 2148000, int(q/2)],
        [868000, 1735800, 6076000, int(q/2)], 
        [947800, 1895600, 6635000, int(q/2)],

    ]
    alldelta1 = [
        [34000, 34000, 34000, 560000],
        [148000, 148000, 148000, 2290000],
        [426000, 426000, 426000, 6500000],
        [464000, 464000, 464000, 7100000],
    ]
    
    # step 1 to recover the absolute values
    # the parameters we chose for k around  q/32 q/16 q/4 q/2  
    k = allk1[wk]
    delta = alldelta1[wk]
    signals = []
    # for each k and delta, we get the corresponding signals
    # print("First parse:")
    query = []
    # for i in range(len(k)):
    #     sig, q = getsig(k[i], n, delta[i])
    #     signals.append(sig)
    #     query.append(q)
    
    pool = Pool(4)
    r = pool.starmap(getsig, zip(k, repeat(n), repeat(q), delta))
    pool.close()
    pool.join()
    for i in range(len(k)):
        signals.append(r[i][0])
        query.append(r[i][1])

    print("queries: {} {}".format(query, sum(query)))

    # the code of each value in [0,15] from gding12
    code = [0, 1, 2, 3, 4, 5, 6, 7, 12, 13, 14, 15, 8, 9, 10, 11] 
    
    # get the practical code for signals
    checkcode = []
    for i in range(n):
        temp = 0
        for b in range(len(k)):
            temp += 2 ** (b) * signals[4- (b + 1)][i]
        checkcode.append(temp)
    
    # get sB' from checkcode
    sBp = []
    for i in range(n):
        sBp.append(code.index(checkcode[i]))
    # print(sBp)
    # print(list(map(abs, sB)))
    # check whether the absolute values are right
    if sBp != list(map(abs, sB)):
        print("error in first parse")
        print(sB)
        return False, 0
    # else:
    #     print("get the right absolute values \n")
    #     return True, sum(query)

    # set k and delta to get all signs of sB
    allk2   = [70000, 280000, 813000, 888000]
    allbndh = [630000, 2580000, 7310000, 7980000]
    allbndl = [497000, 2020000, 5710000, 6230000]
    k    = allk2[wk]
    bndh = allbndh[wk]
    bndl = allbndl[wk]
    # # print("Second parse:")
    sBp, q = sign_sBp(n, q, sB, sBp, k, bndh, bndl)
    print("query: {}".format(q))

    if sBp == list(sB):
        print("get the True sB")
        query = sum(query) + q
        print("all queries: ", query)
        # print(sBp)
        return True, query
    else:
        print("failed in second parse")
        return False, 0


if __name__ == "__main__":
    if not (int(argv[1]) in [128,256,512,1024]):
        print("error argv", argv[1])
        exit()
    n = int(argv[1])    # which parameters we use
    wk = {128:0, 256:1, 512:2, 1024:3}
    allnq = {128:2255041, 256:9205761, 512:26038273, 1024:28434433}
    #n = n[wk] 
    q = allnq[n]
    sigma = 4.19
    print("parameters: n = {:d}, q = {:d}, sigma = {:f}".format(n, q, sigma))
    print("======================")

    c = 1

    alltime = 0
    allq = 0
    countsucc = 0
    for seed in range(c):
        start = time.time()
        # print("======================")
        # print("seed = ", seed)
        random.seed(seed + time.time())
        # seed = 3
        a = Poly.uniform(n, q)
        global f, execution
        f = Poly(n,q)
        execution = Ding19(n, q, sigma, seed)
        sB = execution.sj
        # test = [-3, -2, -1, 4, 1, 0, 2, 3, -1, 7, -1, -2, -10, -1, -5, 2, -1, 8, -11, -2, 7, -2, 1, -2, -2, -5, -3, 0, 3, 6, 2, -8, 4, 6, 1, -5, 8, 3, 1, 0, -3, 5, -3, -2, 4, 2, 5, -1, 4, 0, 0, -14, 6, 0, -8, -4, 4, -1, -8, -1, -5, 6, -1, -11, 4, 2, -1, 3, 1, -2, 4, -1, -1, 12, 1, 2, 2, -5, 1, 1, 2, -2, 2, -7, -7, 1, -2, -7, -5, -1, 0, 7, -2, 7, 4, -1, -3, 2, 1, 4, -8, -7, -4, 2, 1, -1, -1, -5, 3, -4, -5, -4, 1, -3, 0, -1, -3, 7, -4, -2, 5, 7, 1, -1, 4, 3, 0, -7, 6, 9, -2, 8, -9, 5, 0, 2, -5, -2, 1, 1, -2, -9, 0, 3, 3, -2, -3, 3, 0, 3, -1, -7, 4, -7, -1, 10, 5, -1, 2, -4, 1, 0, 2, -4, -13, -2, 3, -2, 2, 3, -1, 2, -5, -4, 0, -7, 4, 3, -9, 2, 0, -3, 2, -2, -1, 4, -3, -1, 2, 2, 0, -3, -1, 1, -5, -4, 6, 3, 3, 2, 1, 2, 9, -4, -1, -4, 5, 4, -1, -4, -2, 0, -4, 0, -4, 1, -6, -8, 4, 9, -1, 4, 1, -6, -5, 3, 3, 4, 0, 4, 1, -4, 0, -3, -1, 2, 0, -3, 1, 0, 0, -4, 2, 3, 1, -5, 2, -1, 0, 6, 0, -5, 5, 12, 3, -6, -2, -1, 1, -1, 4, 0, -7, -7, 0, 2, 7, 1, 0, 0, -4, 3, -3, -3, 1, 6, 5, -5, 5, -5, 1, 5, -1, -1, 2, 0, 0, -1, 5, 0, -4, 2, -9, -4, 0, -3, -2, -1, -1, 3, 4, 0, -8, 3, -3, -4, -5, -11, -1, -2, -6, 2, 1, -5, 6, 2, -2, 6, -2, -4, -4, -1, 1, 0, -2, -9, 8, -3, -4, -1, 9, -1, 4, 1, -2, -4, 4, 2, -4, 4, 4, -2, 0, 2, 4, -4, -3, 5, -1, -8, -1, -1, -1, -2, 8, 8, 2, 2, 3, 3, -1, 2, -3, 0, 5, 2, -1, -4, -3, 3, -6, -2, 4, -2, -2, 1, -5, 2, -6, -3, -6, -3, 2, -4, 0, 0, -1, 2, 6, -2, -1, -4, 6, -4, 0, 7, 3, -3, -3, 5, 1, 1, 2, -1, 0, 4, 5, 2, -5, 8, 11, -5, 2, -1, -1, 1, -3, -1, 4, 2, 7, -1, 10, 3, -2, 4, 2, 0, -2, 5, 2, 2, -3, 3, 0, -2, 0, -5, -4, 1, -7, 0, -2, 7, 3, -3, -1, 3, 3, -1, 7, -3, -3, 8, 2, -6, -4, 4, -6, 1, -2, 3, 0, 0, 4, 3, -3, -4, -4, -1, 2, 6, -4, 7, 3, -6, 0, -2, 0, -6, -3, 1, 5, -2, -1, 3, -4, 8, -7, 0, 2, 0, -3, 7, 0, 10, 2, 4, 4, 3, -3, -3, -6, -1, 6, -3, -1, -5, 2, 4, 0, 4]
        # for i in range(len(test)):
        #     sB[i] = test[i]
        # sB[0] = 14
       
        print("sB = \n", sB)
        print("max s is {}".format( max(map(abs, sB))))
        succ, query = improvesla(n, q, sB, wk[n])
        end = time.time()
        if succ != False:
            seconds = end - start
            alltime += seconds
            allq += query
            countsucc += 1
            print("time: {:.5f}".format(seconds))
        else:
            print("failed ", seed)
            exit()
        print("count ", seed, "\n")
    print("average: {} {} {}".format(allq / c, alltime / c, countsucc / c))
