import math
from gpoly import Poly
import helper
import random
import datetime
import time
import math
import sys

# https://eprint.iacr.org/2012/688.pdf
class Ding12(object):
    def __init__(self, n, q, sigma):
        self.n = n
        self.q = q
        self.sigma = sigma
        self.a = Poly.uniform(self.n, self.q)
        self.sA = Ding12.gen_secret(self.n, self.q, self.sigma)
        self.eA = Ding12.gen_pubkey_error(self.n, self.q, self.sigma)
        self.sB = Ding12.gen_secret(self.n, self.q, self.sigma)
        
    @staticmethod
    def calculate_sigma(n, q, alpha):
        return alpha * q / math.sqrt(n)

    @staticmethod
    def gen_secret(n, q, sigma):
        return Poly.discretegaussian(n, q, sigma)

    @staticmethod
    def gen_pubkey_error(n, q, sigma):
        return Poly.discretegaussian(n, q, sigma)

    @staticmethod
    def gen_shared_error(n, q, sigma,pA=0):
        if pA:
            seed = hash(str(pA))
        return Poly.discretegaussian(n, q, sigma,seed)

    @staticmethod
    def sig(q, v):
        # v = v % q
        if v > math.floor(q / 4.0 + 0.5) and v < q - math.floor(q / 4):
            return 1
        else:
            return 0

    def signal(self, v):
        return [Ding12.sig(self.q, v[i]) for i in range(self.n)]

    def mod2(self, v, w):
        r = [0 for i in range(self.n)]
        for i in range(self.n):
            r[i] = int(v[i] + w[i] * (self.q - 1) / 2)
            r[i] %= self.q
            r[i] %= 2
        return r

    def alice_init(self):
        self.pA = self.a * self.sA + 2 * self.eA
        return self.pA

    def bob(self, pA):
        self.eB = Ding12.gen_pubkey_error(self.n, self.q, self.sigma)
        self.gB = Ding12.gen_shared_error(self.n, self.q, self.sigma, pA)
        self.pB = self.a * self.sB + self.eB + self.eB
        self.kB = pA * self.sB + self.gB + self.gB
        # print("max e ", max(map(abs, self.gB)))
        self.wB = self.signal(self.kB)
        self.skB = self.mod2(self.kB, self.wB)
        return (self.pB, self.wB, self.skB)
    
    def alice_resp(self, pB, wB): # runtime : n^2
        self.gA = Ding12.gen_shared_error(self.n, self.q, self.sigma)
        self.kA = pB * self.sA + self.gA + self.gA
        self.skA = self.mod2(self.kA, wB)
        return self.skA

# def checks(n, q, sB, signals, l, param):
def getabs_sBp(n, q, sB, signals, l, param):
    def sig(v):
        v = v % q
        return 1 if (v > math.floor(q / 4.0 + 0.5) and v < q - math.floor(q / 4)) else 0
            
    def inornot(list):
        def foo(a):
            a = abs(a)
            return 0 if a in list else 1
        return foo
     
    def addtwos(sB):
        p    = Poly(n, q)
        p[0] = 1
        p[1] = 1
        return sB * p

    # s = [ i for i in range(2**l)]
    # presig = {}
    # stosig = []
    # for i in range(l):
    #     a = {0: [], 1: []}
    #     temp = list(map(sig, map(lambda x: x*param[i], s)))
    #     print(temp)
    #     stosig.append(temp)
    #     for j in range(len(temp)):
    #         a[0].append(j) if temp[j] == 0 else a[1].append(j)
    #     print(i, ' ', a)
    #     # print(len(a[0]), ' ', len(a[1]))
    #     presig[i] = a

    # print("here: ", presig)
    # for i in stosig:
    #     print(i)

    code = [0, 8, 4, 12, 2, 10, 6, 14, 3, 11, 7, 15, 1, 9, 5, 13]
    if l == 5: code = [0, 16, 8, 24, 4, 20, 12, 28, 6, 22, 14, 30, 2, 18, 10, 26, 3, 19, 11, 27, 7, 23, 15, 31, 5, 21, 13, 29, 1, 17, 9, 25]
    
    ## +
    # code = [0, 3, 6, 5, 12, 15, 10, 9, 8, 11, 14, 13, 4, 7, 2, 1]
    
    # code = []
    # for i in range(len(s)):
    #     sum = 0
    #     for b in range(l):
    #         sum += 2**(b) * stosig[b][i]
    #     code.append(sum)
    # print(code)
    # print(sorted(code))

    # flag = True

    # if l == 5:
    #     sB = addtwos(sB)
    #     # print(sB)
    # print(max(list(map(abs, sB))))

    # for i in range(l):
    #     check = list(map(inornot(presig[i][0]), sB))
    #     if check != signals[i]:
    #         flag = False
        # if len(presig[i][0]) != len(presig[i][1]):
        #     flag = False

    # codes = [code[abs(sB[i])] for i in range(n)]
    # print(codes)
    # code = [0, 1, 2, 7, 4, 13, 14, 11, 8, 9, 10, 15, 12, 5, 6, 3]
    checkcode = []
    for i in range(n):
        sum = 0
        for b in range(l):
            sum += 2**(b) * signals[b][i]
        checkcode.append(sum)
    # print(checkcode)
    
    # if checkcode != codes: flag = False

    # print("right") if (flag == True) else sys.exit()

    sBp = []
    for i in range(n):
        sBp.append(code.index(checkcode[i]))
    # print(sBp)
    # if l == 5:
    #     x = Poly(n, q)
    #     x[0] = 1
    #     x[1] = 1
    #     sB = sB * x 
    # print(sB)
    # if sBp == list(map(abs, sB)):
    #     print("True")
    return sBp

def collect_signals(n, q, alpha, a, sB, istar, t, l):
    global execution
    global query

    pA = Poly(n, q)
    f  = Poly(n, q)
    f[0] = 1
    param = []
    signals = []
    if l == 5:
        f[istar] = 1
    k = [550, 1050, 4000, 8192]
    if l == 5: k = [260,525,1050,4000,8192]
    for i in range(l):
        # pA[0] = int(q/2**(i+1)) - b[i]
        pA[0] = k[i]
        param.append(pA[0])
        (pB, wB, skB) = execution.bob(pA * f)
        query += 1
        signals.append(wB)
    sBp = getabs_sBp(n, q, sB, signals, l, param)
    # print(sBp)
    # if sBp == list(map(abs, sB)):
    #     print("Get right abs sB", l)
    # else:
    #     print("error in abs sB", l)  
    #     sys.exit()
    return sBp


def collect_abs(n, q, alpha, a, sB, istar, t, l):
    coeffs_abs = collect_signals(n, q, alpha, a, sB, istar, t, l)
    return coeffs_abs
    
def strarray(a):
    s = "["
    for x in a:
        if isinstance(x, bool): s += " T" if x else " F"
        elif isinstance(x, int): s += "{:2d}".format(x)
        elif isinstance(x, str): s += "{:2s}".format(x)
        elif x is None: s += "  "
        else: assert False, "Invalid type " + x
        s += " "
    s += "]"
    return s

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

def fluhrer_attack_new(n, q, alpha, a, sB, t):
    global zero
    coeffs_abs = collect_abs(n, q, alpha, a, sB, 0, t, 4)
    # print("                           ", strarray(range(n)))
    # print("istar = ", 0, "coeffs[istar] = ", strarray(coeffs_abs))
    # print(coeffs_abs)
    zero_count = get_zeros(coeffs_abs,n)
    zero  += zero_count
    # print(zero_count)
    # zero_count = 4
    MAX_ISTAR = zero_count + 2
    coeffs = list(range(MAX_ISTAR))
    coeffs[0] = coeffs_abs
    for istar in range(1,MAX_ISTAR):
        coeffs[istar] = collect_abs(n, q, alpha, a, sB, istar, t, 5)
        # print("istar = ", istar, "coeffs[istar] = ", strarray(coeffs[istar]))
    sign_comp = [[None for j in range(n)] for istar in range(n)]
    for istar in range(1, MAX_ISTAR):
        for i in range(istar, n):
            if coeffs[0][i] != 0 and coeffs[0][i - istar] != 0:
                if coeffs[istar][i] == coeffs[0][i] + coeffs[0][i - istar]: sign_comp[i][i - istar] = "S"
                else: sign_comp[i][i - istar] = "D"
        for i in range(istar):
            if coeffs[0][i] != 0 and coeffs[0][(i - istar) % n] != 0:
                if coeffs[istar][i] == coeffs[0][i] - coeffs[0][(i - istar) % n]:
                    sign_comp[i][(i - istar) % n] = "S"
                else:
                    sign_comp[i][(i - istar) % n] = "D"
    coeffs_signed = Poly(n, q)
    for i in range(n): coeffs_signed[i] = coeffs[0][i]
    for i in range(0, n):
        if coeffs_signed[i] != 0:
            pos_votes = 0
            neg_votes = 0
            for j in range(0, i):
                if coeffs_signed[j] < 0:
                    if sign_comp[i][j] == "S": neg_votes += 1
                    if sign_comp[i][j] == "D": pos_votes += 1
                elif coeffs_signed[j] > 0:
                    if sign_comp[i][j] == "S": pos_votes += 1
                    if sign_comp[i][j] == "D": neg_votes += 1
            if neg_votes > pos_votes: coeffs_signed[i] *= -1
    # print("sB            = ", strarray(sB))
    # print("coeffs_signed = ", strarray(coeffs_signed))
    return sB == coeffs_signed or sB == -1 * coeffs_signed

if __name__ == "__main__":
    n = 1024
    q = 16385
    sigma = 3.197
    t = 100
    alltime = 0
    succ = 0
    count = 10
    print("parameters: n = {:d}, q = {:d}, sigma = {:f}".format(n, q, sigma))

    global query
    global zero
    query = 0
    zero = 0
    now = int(time.time())
    for seed in range(count):
        start = time.time()
        print("======================")
        # seed = 1
        print("seed = ", seed)
        random.seed(seed + now)
        # random.seed(seed)
        seed += now
        a = Poly.uniform(n, q)
        sB = Poly.discretegaussian(n, q, sigma, seed)
        # sB = Poly.discretegaussian(n, q, sigma)
        # sB[0] = 15
        # print("     ", strarray(range(n)))
        # print("sB = ", strarray(sB))
        # print(max(list(map(abs, sB))))
        global execution
        execution = Ding12(n, q, sigma)
        execution.a = a
        execution.sB = sB
        if fluhrer_attack_new(n, q, sigma, a, sB, t) == True:
            succ += 1
        # fluhrer_attack_new(n, q, sigma, a, sB, t)
        end = time.time()
        cost = end - start
        alltime += cost
        # hours, rem = divmod(end-start, 3600)
        # minutes, seconds = divmod(rem, 60)
        # print("{:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds))

    print("succ:", succ / count)
    print("all queries: ", query)
    print("average: {} {} {}".format(alltime / count, query / count, zero / count))
