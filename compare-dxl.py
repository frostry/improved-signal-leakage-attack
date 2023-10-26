import math
from gpoly import Poly
# from poly import Poly   # use mulmont
import helper
import random
import datetime
import time

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
        self.gB = Ding12.gen_shared_error(self.n, self.q, self.sigma,pA)
        self.pB = self.a * self.sB + self.eB + self.eB
        self.kB = pA * self.sB + self.gB + self.gB
        self.wB = self.signal(self.kB)
        self.skB = self.mod2(self.kB, self.wB)
        return (self.pB, self.wB, self.skB)

    def alice_resp(self, pB, wB): # runtime : n^2
        self.gA = Ding12.gen_shared_error(self.n, self.q, self.sigma)
        self.kA = pB * self.sA + self.gA + self.gA
        self.skA = self.mod2(self.kA, wB)
        return self.skA



def collect_signals(n, q, alpha, a, sB, istar, t):
    global execution
    global query
    signals = list(range(q // t))
    for k in range(0, q // t):
        signals[k] = list(range(n))

    # collect the signals
    pA = Poly(n,q)
    f = Poly(n,q)
    f[0] = 1
    if istar is not None: f[istar] = 1
    for k in range(0, q // t):
        pA[0] = k*t
        (pB, wB, skB) = execution.bob(f * pA)
        query += 1
        for i in range(n):
            signals[k][i] = wB[i]
    return signals

def collect_abs(n, q, alpha, a, sB, istar, t):
    signals = collect_signals(n, q, alpha, a, sB, istar, t)
    coeffs_abs = list(range(n))
    for i in range(n):
        f = [signals[k][i] for k in range(int((q-85)/100))]
        coeffs_abs[i] = helper.likeliest_abs_secret_from_signals_count(f, Ding12.sig, sigma)
        if istar == 0 and coeffs_abs[i] != abs(execution.sB[i]):
            print("error: ", coeffs_abs[i], execution.sB[i], f)
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
    coeffs_abs = collect_abs(n, q, alpha, a, sB, 0, t)
    # print("                           ", strarray(range(n)))
    # print("istar = ", 0, "coeffs[istar] = ", strarray(coeffs_abs))
    zero_count = get_zeros(coeffs_abs,n)
    zero += zero_count
    # zero_count = 4
    MAX_ISTAR = zero_count + 2
    coeffs = list(range(MAX_ISTAR))
    coeffs[0] = coeffs_abs
    for istar in range(1,MAX_ISTAR):
        coeffs[istar] = collect_abs(n, q, alpha, a, sB, istar, t)
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
    print("sB            = ", strarray(sB))
    print("coeffs_signed = ", strarray(coeffs_signed))
    return sB == coeffs_signed or sB == -1 * coeffs_signed

if __name__ == "__main__":
    n = 1024
    q = 16385
    sigma = 3.197
    t = 100
    alltime = 0
    count = 1
    global query 
    global zero 
    zero = 0
    query = 0
    print("parameters: n = {:d}, q = {:d}, sigma = {:f}".format(n, q, sigma))

    now = int(time.time())
    for seed in range(count):
        start = time.time()
        print("======================")
        print("count = ", seed)
        random.seed(seed + now)
        seed = now + seed
        a = Poly.uniform(n, q)
        sB = Poly.discretegaussian(n, q, sigma, seed)
        # print("     ", strarray(range(n)))
        # print("sB = ", strarray(sB))
        global execution
        execution = Ding12(n, q, sigma)
        execution.a = a
        execution.sB = sB
        print(fluhrer_attack_new(n, q, sigma, a, sB, t))
        end = time.time()
        cost = end-start
        alltime += cost
        hours, rem = divmod(cost, 3600)
        minutes, seconds = divmod(rem, 60)
        print("{:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds))
    hours, rem = divmod(alltime/count, 3600)
    minutes, seconds = divmod(rem, 60)
    print("average: {:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds))
    print("all query: ", query)
    print("average: ", query / count, " ", zero / count)