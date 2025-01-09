import math
from gpoly import *
import random
from ctypes import *
# import cProfile
import time
from itertools import repeat
from multiprocessing import Pool, set_start_method
import platform
import secrets

class Ding19(object):
    def __init__(self, n, q, sigma, seed):
        self.n = n
        self.q = q
        self.sigma = sigma
        self.a = Poly.uniform(self.n, self.q)
        self.si = Ding19.gen_secret(self.n, self.q, self.sigma)
        self.ei = Ding19.gen_pubkey_error(self.n, self.q, self.sigma)
        self.sj = Ding19.gen_secret(self.n, self.q, self.sigma, seed)
        self.ej = Ding19.gen_pubkey_error(self.n, self.q, self.sigma)


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
        if v > math.floor(q / 4.0 + 0.5) and v < q - math.floor(q / 4):
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
        
    def hash1(self, Pa):
        seed = hash(str(Pa))
        return Poly.discretegaussian(self.n, self.q, self.sigma, seed)
        
    def hash2(self, xs):
        seed = hash(str(xs))
        return Poly.discretegaussian(self.n, self.q, self.sigma, seed)

    def alice_init(self):
        self.xi = self.a * self.si + 2 * self.ei
        return self.xi

    #def bob(self, Pi, Pj, xi, simplified=True):
    def bob(self, Pa):
        self.Pb = self.a * self.sj + 2 * self.ej
        es = Ding19.gen_pubkey_error(self.n, self.q, self.sigma)
        rs = Ding19.gen_secret(self.n, self.q, self.sigma, secrets.randbits(32))
        self.xs = self.a * rs + 2 * es  
        #print(self.xs)
        #c = self.hash1(Pi, Pj, xi)
        #d = self.hash2(Pi, Pj, xi, self.yj)
        c = self.hash1(Pa)
        d = self.hash2(self.xs)
        
        self.eb = Ding19.gen_shared_error(self.n, self.q, self.sigma)

        Pabar = Pa + self.a * c 
        self.kb = Pabar * (self.sj + d) + 2 * self.eb
    
        self.wj = self.signal(self.kb)
        self.skj = self.mod2(self.kb, self.wj)
        
        return (self.Pb, self.xs, self.wj, self.skj)
        
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

# def getsig(k, n, kn_bnd, signals, query, r):
def getsig(k, n, kn_bnd):
    global execution
    global f

    signals = [None for i in range(n)]
    a = execution.a

    pa = k * f
    # print(pa)
    got_signals = 0
    query = 0
    
    # limit = 5
    # start = time.time()
    # while got_signals < n:
    #     (Pb, xs, wj, skj) = execution.bob(pa)
    #     query += 1
    #     # print(query)
    #     c = execution.hash1(pa)
    #     d = execution.hash2(xs)
    #     known = c * Pb + a * c * d + d * pa
    #     for i in range(n):
    #         if (known[i] <= kn_bnd  or known[i] >= (q - kn_bnd)) and signals[i] == None:
    #             signals[i] = wj[i]
    #             got_signals += 1
    #     print(got_signals)

    #     end = time.time()
    #     if end - start > limit:
    #     #     time.sleep(0.1)
    #         print("time out")
    #     #     start = time.time()
    #         break
    # r.put([signals, query])
    # return signals, query
    
    while got_signals < n:
        (Pb, xs, wj, skj) = execution.bob(pa)
        query += 1
        c = execution.hash1(pa)
        d = execution.hash2(xs)
        known = c * Pb + a * c * d + d * pa
        for i in range(n):
            if (known[i] <= kn_bnd  or known[i] >= (q - kn_bnd)) and signals[i] == None:
                signals[i] = wj[i]
                got_signals += 1
                # print(got_signals)
    return signals, query

def sign_sBp(n, q, sB, sBp, *para):
    global execution
    global f

    signals = [None for i in range(n)]
    a = execution.a

    k = para[0]
    bndh = para[1]
    bndl = para[2]

    pa = k * f
    got_signals = 0
    query = 0

    while got_signals < n:
        (Pb, xs, wj, skj) = execution.bob(pa)
        query += 1
        c = execution.hash1(pa)
        d = execution.hash2(xs)
        known = c * Pb + a * c * d + d * pa
        # print(known)
        for i in range(n):
            # if sBp[i] == 0 and signals[i] == None:
            #     signals[i] = 0
            #     got_signals += 1
            if bndl <= known[i] <= bndh and signals[i] == None:
                signals[i] = wj[i]
                got_signals += 1
        # print(got_signals)
    # print("query: ", query)
    # print(got_signals)
    for i in range(n):
        if signals[i] == 0 and sBp[i] != 0:
            sBp[i] = -sBp[i]    
    return [sBp, query]

def improvesla(n, q, sB):
    global f
    f[0] = 1
    
    # signals = [[None for i in range(n)] for i in range(4)]
    # query = [0  for i in range(4)]

    # step 1 to recover the absolute values
    # the parameters we chose for k around  q/32 q/16 q/4 q/2 
    k = [252000, 503800, 1764000, int(q/2)]
    delta = [122000, 122000, 122000, 1887000]
    
    signals = []
    # for each k and delta, we get the corresponding signals
    # print("First parse:")
    query = []
    # for i in range(len(k)):
    #     sig, q = getsig(k[i], n, delta[i])
    #     signals.append(sig)
    #     query.append(q)
    
    pool = Pool(4)
    r = pool.starmap(getsig, zip(k, repeat(n), delta))
    pool.close()
    pool.join()
    for i in range(len(k)):
        signals.append(r[i][0])
        query.append(r[i][1])
    # r = Queue()
    # while None  in signals[0]:
    #     p = Process(target=getsig, args=(k[0], n, delta[0], signals[0], query[0], r))
    #     p.start()
    #     results = r.get()
    #     signals[0] = results[0]
    #     query[0]   = results[1]
    #     p.join()
    #     # sys.exit()

    # print(signals[0])
    # print(query[0])
    # # for i in range(len(k)):
    # #     signals.append(r[i][0])
    # #     query.append(r[i][1])

    print("queries: {} {}".format(query, sum(query)))
    # # print(signals[3])
    
    # sys.exit()

    # the code of each value in [0,15] from gding12
    code = [0, 1, 2, 3, 4, 5, 6, 7, 12, 13, 14, 15, 8, 9, 10, 11] 
    
    # get the practical code for signals
    checkcode = []
    for i in range(n):
        temp = 0
        for b in range(len(k)):
            temp += 2 ** (b) * signals[4- (b + 1)][i]
        checkcode.append(temp)
    # print(checkcode)
    
    # get sB' from checkcode
    sBp = []
    for i in range(n):
        sBp.append(code.index(checkcode[i]))

    # print(list(map(abs, sB)))
    # check whether the absolute values are right
    if sBp != list(map(abs, sB)):
        print("error in first parse")
        print(sB)
        return False, 0
    # else:
        # print("get the right absolute values \n")
    #     return True, sum(query)

    # time.sleep(5)
    # set k and delta to get all signs of sB, k ~~ q/32
    k    = 236000
    bndh = 2120000
    bndl = 1656000
    # print("Second parse:")
    sBp,   q2 = sign_sBp(n, q, sB, sBp, k, bndh, bndl)
    print("query: {}".format(q2))

    if sBp == list(sB):
        print("get the True sB")
        query = sum(query) + q2
        print("all queries: ", query)
        # print(sBp)
        return True, query
    else:
        print("failed in second parse")
        return False, 0

def test_random():
    global execution
    global f
    a = execution.a

    f[0] = 1
    pa = 252000 * f
    r  = {}
    for i in range(1*10**3):
        (Pb, xs, wj, skj) = execution.bob(pa)
        c = execution.hash1(pa)
        d = execution.hash2(xs)
        known = c * Pb + a * c * d + d * pa
        if known[0] not in r:
            r[known[0]] = 0
        r[known[0]] += 1
    print(sorted(r.items(),key=lambda x:x[0],reverse=False))
    print(max(r.values()))


if __name__ == "__main__":
    n = 512
    q = 7557773
    sigma = 3.192 
    print("parameters: n = {:d}, q = {:d}, sigma = {:f}".format(n, q, sigma))
    print("======================")

    if platform.system() == 'Darwin':
        set_start_method("fork")
    
    c = 1
    alltime = 0
    allq = 0
    for seed in range(c):
        start = time.time()
        # print("seed = ", seed)
        random.seed(seed + time.time())
        # seed = 3
        a = Poly.uniform(n, q)
        global f, execution
        f = Poly(n,q)
        execution = Ding19(n, q, sigma, seed)
        sB = execution.sj
        # sB[0] = 14
        print("sB = \n", sB)
        # print("max s is {}".format( max(map(abs, sB))))
        
        # test_random()

        succ, query = improvesla(n, q, sB)
        end = time.time()
        if succ != False:
            seconds = end - start
            alltime += seconds
            allq += query
            print("time: {:.5f}".format(seconds))
        else:
            print("failed ", seed)
            exit()
        print("count ", seed, "\n")
    print("average: {} {}".format(allq / c, alltime / c))
