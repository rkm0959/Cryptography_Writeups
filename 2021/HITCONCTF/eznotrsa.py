from Crypto.Cipher import AES, PKCS1_OAEP, PKCS1_v1_5
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import pad, unpad
from Crypto.Util import Counter
from Crypto.Util.number import inverse, long_to_bytes, bytes_to_long, isPrime, getPrime, getRandomRange, sieve_base
from tqdm import tqdm
from pwn import *
from sage.all import *
import gmpy2, pickle, itertools, sys, json, hashlib, os, math, time, base64, binascii, string, re, struct, datetime, subprocess
import numpy as np
import random
import multiprocessing as mp
from base64 import b64encode, b64decode
from sage.modules.free_module_integer import IntegerLattice
from Crypto.Hash import SHA3_256, HMAC, BLAKE2s
from Crypto.Cipher import AES, ARC4, DES

class Twister:
    N = 624
    M = 397
    A = 0x9908b0df

    def __init__(self):
        self.state = [ [ (1 << (32 * i + (31 - j))) for j in range(32) ] for i in range(624)]
        self.index = 0
    
    @staticmethod
    def _xor(a, b):
        return [x ^ y for x, y in zip(a, b)]
    
    @staticmethod
    def _and(a, x):
        return [ v if (x >> (31 - i)) & 1 else 0 for i, v in enumerate(a) ]
    
    @staticmethod
    def _shiftr(a, x):
        return [0] * x + a[:-x]
    
    @staticmethod
    def _shiftl(a, x):
        return a[x:] + [0] * x

    def get32bits(self):
        if self.index >= self.N:
            for kk in range(self.N):
                y = self.state[kk][:1] + self.state[(kk + 1) % self.N][1:]
                z = [ y[-1] if (self.A >> (31 - i)) & 1 else 0 for i in range(32) ]
                self.state[kk] = self._xor(self.state[(kk + self.M) % self.N], self._shiftr(y, 1))
                self.state[kk] = self._xor(self.state[kk], z)
            self.index = 0

        y = self.state[self.index]
        y = self._xor(y, self._shiftr(y, 11))
        y = self._xor(y, self._and(self._shiftl(y, 7), 0x9d2c5680))
        y = self._xor(y, self._and(self._shiftl(y, 15), 0xefc60000))
        y = self._xor(y, self._shiftr(y, 18))
        self.index += 1

        return y
    
    def getrandbits(self, bit):
        return self.get32bits()[:bit]

class Solver:
    def __init__(self):
        self.equations = []
        self.outputs = []
    
    def insert(self, equation, output):
        for eq, o in zip(self.equations, self.outputs):
            lsb = eq & -eq
            if equation & lsb:
                equation ^= eq
                output ^= o
        
        if equation == 0:
            return

        lsb = equation & -equation
        for i in range(len(self.equations)):
            if self.equations[i] & lsb:
                self.equations[i] ^= equation
                self.outputs[i] ^= output
    
        self.equations.append(equation)
        self.outputs.append(output)
    
    def solve(self):
        num = 0
        for i, eq in tqdm(enumerate(self.equations)):
            if self.outputs[i]:
                # Assume every free variable is 0
                num |= eq & -eq
        
        state = [ (num >> (32 * i)) & 0xFFFFFFFF for i in range(624) ]
        return state

POL = PolynomialRing(ZZ, 'x')
x = POL.gen()

n, q = 263, 128

def list_to_pol(l):
    ret = 0
    for i in range(len(l)):
        ret += l[i] * (x ** i)
    return ret

def randomdpoly(d1, d2):
    result = d1 * [1] + d2 * [-1] + (n - d1 - d2) * [0]
    random.shuffle(result)
    return list_to_pol(result)

def convolution(f, g):
    return (f * g) % ((x ** n) - 1)

def balancedmod(f, q):
    coefs = f.coefficients(sparse=False)
    while len(coefs) < n:
        coefs.append(0)
    g = list(((coefs[i] + q//2) % q) - q//2 for i in range(n))
    return list_to_pol(g)

state_1400 = (2147483648, 3575941739, 2129811211, 1434746901, 33280334, 1426607318, 870068110, 1729685034, 1997091661, 4127880471, 774500132, 2822266559, 487407463, 3413919974, 133630759, 285867513, 1320346030, 3565126752, 1186117558, 443751305, 1568728130, 223057019, 2880399869, 1015809794, 1850071066, 1357366613, 3937708394, 2571894108, 871157479, 3466049557, 2556186252, 279454580, 643583743, 422921945, 2724422054, 2720056941, 2983831652, 2923066508, 4106583972, 379660542, 3204932207, 687932826, 308064632, 4146605502, 2028865494, 1949287265, 1439714868, 3960607326, 3725723100, 728613595, 4022562243, 940664112, 3794433843, 3394618089, 1975695495, 867898689, 1243690720, 1226717095, 4054366440, 2272200495, 1915395651, 96927682, 3603881286, 588058185, 2638798589, 3678681290, 265544620, 3684064608, 3758496973, 3011329373, 3429395624, 123167539, 2302230972, 1771136571, 2024902818, 2534882203, 860482027, 952761544, 1311551242, 423705476, 3047754557, 3995238149, 883533918, 3650041539, 572827877, 2440129137, 2561644522, 3545025048, 1356376233, 211685688, 3426018854, 3935137126, 3609708529, 4243293676, 1319835998, 2741586252, 498788213, 759519278, 1400460671, 3350071023, 3333656123, 3755696540, 1809442715, 2549196949, 524831900, 518978322, 2500725752, 385138172, 315357527, 859524746, 291249283, 1721860501, 1781704940, 4129852545, 1191856707, 2252316040, 2183175954, 3219843376, 1611103864, 4258360662, 275150801, 777775571, 3248193991, 160898803, 885924555, 182595302, 1250735541, 3383490277, 2682843662, 2429939998, 1334645552, 2883435774, 1166812851, 4221923800, 1691409971, 1023881299, 1643031582, 705006686, 2045586719, 1382334829, 1178264868, 2810271246, 2985764975, 3207875310, 1929377912, 2408304068, 1473684786, 2668024405, 2818227477, 374552560, 1292957975, 3270950986, 3866672968, 3012402395, 2432240445, 2768697978, 2516520750, 2116420949, 4206643105, 2561146040, 182028169, 947697549, 4012556840, 2661730153, 1984660535, 17535693, 514128665, 320518761, 642430589, 3290898460, 2444105049, 864267095, 1723903378, 3445243903, 2264373916, 431727517, 1075582756, 4098272464, 1314806726, 1223663875, 384927800, 3865458580, 3069120720, 3974964092, 2480051874, 3287109339, 3167478496, 2609431557, 1087447469, 1387986578, 1998015119, 2257802262, 1374957790, 2980487815, 371712530, 2927818689, 1236433598, 3593330047, 3817462434, 154432403, 3893491044, 2261343180, 2664102235, 2836193768, 466446875, 293427607, 972400150, 2460035844, 69904278, 1250641338, 2285791508, 3078646172, 3957445134, 3532540561, 279506344, 4042599019, 1802823611, 524407536, 1745605122, 1727117248, 628903804, 2732930680, 2602849260, 4143575218, 3979016465, 2880442700, 1244979163, 426646240, 3702291192, 1230552382, 2889058390, 3191565960, 3944443660, 1086026082, 1389748660, 3845719757, 58911887, 3020821535, 3710572770, 1024317563, 795351399, 622243485, 2023973463, 1708480550, 930755747, 536949797, 370314036, 1736032726, 2681853380, 37500712, 3656044141, 3000570994, 632667509, 361240879, 4158532639, 2090339474, 1424753697, 1735127812, 3297628983, 3492992667, 763984949, 2228170116, 681764256, 188092789, 1682556359, 3951385379, 1464966422, 380148822, 3223974275, 1030606225, 272088130, 1691912664, 3764833662, 2790503978, 771066122, 222503125, 2704616949, 1544896273, 2732048545, 616942562, 1163496938, 2708264158, 3235349833, 3686974372, 3213968710, 1654873192, 2716628416, 718403682, 4109219240, 1966028966, 1656013821, 876215067, 2425278432, 1160219793, 853251934, 918041579, 658786644, 3728675233, 619145890, 2975308099, 1381755694, 891522677, 850530101, 2572152447, 3946054117, 1896742056, 1690839434, 2407209970, 1494576948, 1249372425, 4085574520, 1538641604, 1448368996, 4075950874, 420497006, 1631614003, 3745282699, 963523006, 1019803222, 3982337833, 2595369104, 994857266, 2774518738, 1362601913, 1118822462, 3155236569, 1763815292, 4227568196, 1312650853, 3790402863, 2222548581, 559735455, 2322627648, 192671178, 595794111, 463314759, 3351389993, 3391060290, 3974260613, 4128900397, 2555902786, 3611835793, 1892547795, 2505282214, 710492185, 3028280980, 2903505790, 523945106, 206795, 857927601, 1135510736, 425919049, 3442679723, 2393773323, 3436299960, 535330188, 1994756983, 1015090471, 3918275607, 222170778, 1346801709, 1029962040, 1453766036, 3119183150, 22490819, 2132515130, 4074710203, 3704210677, 980423756, 1202406705, 1237410961, 2547605145, 2432475655, 2465486692, 2181195593, 648773066, 1754042126, 3164224354, 3911598553, 2545557071, 2812465865, 2671868561, 3585061264, 3197624979, 1159595992, 1670737625, 2929238121, 382571143, 2893352327, 3281347410, 4215514434, 1624836899, 471424702, 1643811507, 2499802205, 3079632473, 1301225851, 2367869301, 1967827259, 4245275630, 3322866988, 3308899159, 2970740542, 3830999842, 3016467193, 3761493003, 236006988, 2517010180, 4114480657, 2887981757, 2708358269, 906687196, 1847076584, 1742931449, 812330619, 1682930458, 404202562, 3303928435, 4087979168, 3602978797, 689366365, 213272314, 3618988813, 4289522257, 6667465, 1723838457, 1755817445, 1538955178, 3018365560, 1209758954, 1558945893, 9577479, 2359295680, 3195549969, 2065907409, 1788771216, 3870614140, 1094973268, 270573972, 1605041280, 1455185329, 1831088370, 1461744934, 595626844, 3262986969, 1968080386, 3975370406, 2729871254, 183776306, 1363130761, 1841206928, 1526460448, 3740813413, 96608319, 523457195, 315022444, 1700509480, 1226875669, 1819637581, 3996962553, 1871300985, 2189001487, 1859554983, 2100847728, 76782688, 463469767, 1286099656, 2440342928, 2719352325, 883151082, 4019697379, 2000392441, 2966445373, 4220308195, 737689275, 4894870, 1946241078, 4145183542, 4061890147, 776007270, 2600480930, 2822578774, 1546541762, 1202246941, 4292516301, 2580299406, 1314493163, 1592354507, 797989564, 13554204, 1890944426, 904311395, 3478449354, 3417723003, 76096604, 4073169954, 62580237, 2405360354, 800827012, 2081375406, 627272595, 3691499089, 2698102034, 4035484516, 1681958879, 1971631887, 2676255401, 2977516605, 3863114807, 416677861, 1141692591, 1738988183, 2365539961, 1793880796, 2687014811, 3559175965, 573175318, 1930013660, 144951381, 3947724732, 3855937426, 2640473103, 1005809266, 983437892, 1965191224, 4156185134, 2938568980, 3138200709, 2344788080, 202424929, 2063974942, 3239817123, 208551614, 3080305331, 952524310, 1870600745, 2591010872, 1319483422, 3059102756, 4163544234, 490620312, 697694159, 996800420, 1823822957, 2338537485, 3600780744, 2029354400, 3721835569, 3866886674, 2033945850, 360785868, 415631450, 449078354, 2973695459, 3264477468, 1372593491, 1982221997, 3352760018, 4186905321, 1481101344, 2309899887, 1571513868, 1755561303, 1779888643, 2200699928, 1974147831, 1286341551, 3337136241, 291006757, 2146499844, 4219318046, 2974227758, 1981319926, 1465779761, 3374495893, 3323322516, 2721644869, 631952745, 3777583369, 2773269706, 2861540741, 1339168440, 3307966028, 558766288, 2738796507, 121759482, 394629474, 1489486155, 3623180020, 4167399490, 1152996353, 628467132, 1573180588, 1930803162, 2070202448, 3475642433, 484850858, 705467083, 498033860, 3408435273, 1970526070, 1009945034, 2978435677, 1615049428, 340827820, 231557374, 2128332686, 2172341402, 3398720022, 2045629466, 3374342437, 2204194808, 3240162824, 4144761768, 1665919064, 474623662, 327901746, 3196645655, 2083148889, 2463082582, 1167751932, 2076853872, 4083872227, 1413199283, 0)
enc = [20, -17, 38, 39, 39, 23, -56, -41, 18, 50, -45, -57, 15, -55, -4, 62, 15, 55, 15, 63, 35, -20, 25, -26, 33, 17, -59, 27, -37, -3, -6, 48, 0, 47, 6, -30, -25, -60, 42, 29, -31, -12, 37, 35, 35, -20, 34, -33, -63, 18, -59, -40, -5, 30, -15, -15, 22, 16, -5, -2, 55, 7, -17, -13, -23, 28, -25, 42, -37, 28, -32, 46, -56, -54, 35, -12, -1, 3, 41, -54, -9, -58, -44, -6, 50, -62, 16, -30, 13, 50, 34, -6, -24, 16, -62, -20, 23, -2, -49, 20, -31, -45, 35, 22, -23, -10, -21, -58, 19, 14, 53, 11, 19, -2, 18, -45, -10, 41, 23, 38, 55, 34, -12, -16, 44, -36, 29, 61, -17, 8, -30, 9, 43, -57, -38, -24, -16, 56, -34, 13, -10, -14, -38, 49, 16, -42, 29, 45, 39, 5, 51, -12, -40, 25, -63, -11, 16, 62, 23, -39, 32, 51, 14, -3, 56, -42, 46, 58, -56, -46, -23, -48, -37, 13, 59, 29, -20, 32, -22, 34, -8, -33, 26, 46, 24, -39, 36, 34, 14, -49, -18, 19, 5, 29, -24, -29, -19, -14, -31, 49, -46, 54, 46, -54, -31, 46, 30, 38, -24, 14, -34, -51, 21, 56, -43, -36, 51, -36, -9, 12, 39, -6, -48, -14, 13, 3, 10, -51, 11, -44, 62, -58, 14, 55, 28, 43, 45, -57, 37, -16, -33, 8, 24, -43, 22, -14, 13, 13, 17, 6, -48, 39, -61, -18, 58, 43, 57, 51, 48, -8, -45, 17, -53]
pub = [-60, 57, -38, -23, -9, -31, -7, 1, 50, 16, 40, 25, 13, 52, -35, -5, -18, 34, 31, 25, -47, -30, 30, -40, -33, -62, -58, -47, -28, 55, -19, 39, -4, -38, 46, -55, 4, -6, 36, -24, 61, -45, -36, -11, -10, -43, 32, -38, -6, -8, 57, 34, -57, 6, -45, 30, -45, -7, 18, 0, -10, 18, -39, -12, 23, 40, 20, -8, -35, -23, 20, -23, 34, -54, -24, 60, -27, -37, -64, -53, -2, 5, -8, -13, 33, 45, -64, 50, -51, 4, -22, -28, -52, -19, -2, 53, 36, 36, 15, 44, 60, -44, -59, -59, -1, 11, -25, -12, 25, 23, 13, -25, 23, 59, -28, 61, -20, 50, -33, -36, -3, -37, 62, 32, -63, -2, 38, -8, -9, 14, -58, 33, -4, -47, 3, 11, 7, -26, 56, -7, -64, 34, 60, 23, -57, 3, -19, -13, -52, -52, -43, -12, -2, -43, -21, -36, 26, -62, -39, -29, 49, -28, 6, -46, -61, 36, -31, 56, 18, -52, -9, 33, 53, -28, -24, -37, 31, -17, -4, 49, 30, 1, -1, 25, 1, 23, 16, -60, -4, 8, 9, -50, -17, -24, -16, 19, -26, -8, -22, -47, 61, -47, 51, 6, 33, 39, -12, 13, -34, 44, -24, 52, 11, 14, -25, -14, -52, 51, 9, -64, -6, 45, 52, -27, 39, 14, -32, -51, 3, 46, 16, 4, 5, -40, 38, 15, -28, 32, -51, -13, 17, 5, -25, -43, 45, -61, -50, -6, -20, 7, 61, 62, -17, -30, -41, 60, 30, 10, 42, 17, -35, -7, 20]

# Polynomials
enc_pol = 0
for i in range(len(enc)):
    enc_pol += enc[i] * (x ** i)
pub_pol = 0
for i in range(len(pub)):
    pub_pol += pub[i] * (x ** i)

# Import Data
f = open("data", "r")
f.readline()
f.readline()
vals = []

for i in range(200):
    cc = f.readline().split()[0]
    cc = int(cc, 16)
    vals.append(cc)

# Sanity Check
random.setstate((3, state_1400, None))
for i in range(1400):
    random.getrandbits(32)
for i in range(200):
    assert random.getrandbits(240) == vals[i]

# BruteForce Offset
for shift in tqdm(range(1400)):
    random.setstate((3, state_1400, None))
    for _ in range(shift):
        random.getrandbits(32)
    r = randomdpoly(18, 18)
    tt = balancedmod(enc_pol - convolution(pub_pol, r), q)
    coefs = tt.coefficients(sparse = False)
    isok = True
    for i in range(len(coefs)):
        if coefs[i] <= -2 or coefs[i] >= 2:
            isok = False
    if isok:
        print(shift)
        sol = 0
        for i in range(len(coefs)):
            sol += (int(coefs[i]) + 1) * (3 ** i)
        print(sol)
        print(int(sol).to_bytes(64, "big"))


'''
num = 3000
twister = Twister()
outputs = [ rand.getrandbits(32) for _ in range(num) ]
equations = [ twister.getrandbits(32) for _ in range(num) ]

solver = Solver()
for i in tqdm(range(1400, 3000)):
    if i % 8 != 7:
        for j in range(32):
            curv = (vals[(i - 1400) // 8] >> (32 * (i % 8))) & ((1 << 32) - 1)
            solver.insert(equations[i][j], (curv >> (32 - 1 - j)) & 1)

state = solver.solve()
recovered_state = (3, tuple(state + [0]), None)
random.setstate(recovered_state)

for i in range(1400):
    random.getrandbits(32)
for i in range(200):
    assert random.getrandbits(240) == vals[i]
print(recovered_state)
'''