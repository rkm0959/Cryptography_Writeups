from Crypto.Cipher import AES, PKCS1_OAEP, PKCS1_v1_5
from Crypto.PublicKey import RSA
from Crypto.Util.number import inverse, long_to_bytes, bytes_to_long, isPrime, getPrime, GCD
from tqdm import tqdm
from pwn import *
from sage.all import *
import itertools, sys, json, hashlib, os, math, time, base64, binascii, string, re, struct, datetime, subprocess
import numpy as np
import random as rand
import multiprocessing as mp
from base64 import b64encode, b64decode
from sage.modules.free_module_integer import IntegerLattice
from ecdsa import ecdsa

'''
| encrypt(flag) = 672389497129347847615415120361923195258692176123392927264226250379521246332777817771853760225086815757011918365406828747018138436186903655493917519078877156042759074734870780716461334338228173142241581962090866997250787153131686634246671160398195196951962900705325688511086807476383693157010171868814468665226085981264674760386964832416315436215378563203174547406080905847908029276685229773471979785973128185787484913726301113660258765140693355914788061119481837530017302910779137
| Options:
|    [P]rint encrypted flag
|    [R]eveal the parameters
|    [Q]uit
$ r
    e = 65537
    isPrime(p) = True
    isPrime(q) = True
    n = p * q
    (p - 1002)**2 + (q - 205)**2 = 2944384541976463676196896087170081422587651891161440731837296774790205983437395819761947029110404126572573689406494709876156091878136758910742198539244398572206053357257076376842811529286173513260707825041714342202149714644009867513544894462129875096133128842149927615828181488722637087964761878652383631630114200858720081954314329515866355030740545269683204630822908995469238852754949359491905746819769639533764797449484322836249309218158019886598335132181245219500912239931328125
    m = bytes_to_long(flag)
    c = pow(m, e, n)
'''

enc = 672389497129347847615415120361923195258692176123392927264226250379521246332777817771853760225086815757011918365406828747018138436186903655493917519078877156042759074734870780716461334338228173142241581962090866997250787153131686634246671160398195196951962900705325688511086807476383693157010171868814468665226085981264674760386964832416315436215378563203174547406080905847908029276685229773471979785973128185787484913726301113660258765140693355914788061119481837530017302910779137

X = 1002
Y = 205
goal = 2944384541976463676196896087170081422587651891161440731837296774790205983437395819761947029110404126572573689406494709876156091878136758910742198539244398572206053357257076376842811529286173513260707825041714342202149714644009867513544894462129875096133128842149927615828181488722637087964761878652383631630114200858720081954314329515866355030740545269683204630822908995469238852754949359491905746819769639533764797449484322836249309218158019886598335132181245219500912239931328125


res = [5, 17, 29, 229, 1559264295133, 8545601512881220409, 1993953445236547124701695529201]
cnt = [7, 7, 14, 7, 7, 7, 7]
A = []
B = []

for x in res:
    a, b = two_squares(x)
    A.append(a)
    B.append(b)

RES = []
for _ in range(7):
    RES.append([])

def generate(idx, cur, x, y):
    global RES
    if cur == cnt[idx]:
        RES[idx].append((abs(x), abs(y)))
        RES[idx].append((abs(y), abs(x)))
        return
    generate(idx, cur + 1, A[idx] * x + B[idx] * y, B[idx] * x - A[idx] * y)
    generate(idx, cur + 1, B[idx] * x + A[idx] * y, A[idx] * x - B[idx] * y)

for i in range(7):
    generate(i, 0, 1, 0)
    RES[i] = list(set(RES[i]))
    print(len(RES[i]))

print("finish gen")

fin = []

def generate(idx, x, y):
    global fin, RES
    if idx == 7:
        fin.append((abs(x), abs(y)))
        return
    for i in range(len(RES[idx])):
        u, v = RES[idx][i]
        generate(idx + 1, u * x + v * y, v * x - u * y)

generate(0, 1, 0)

print(len(fin))

print("finish fin")

fin = list(set(fin))

print("finish removing duplicates")

for i in tqdm(range(len(fin))):
    u, v = fin[i]
    assert u * u + v * v == goal
    p = u + X
    q = v + Y 
    if isPrime(p) and isPrime(q):
        n = p * q 
        phi = (p - 1) * (q - 1)
        d = inverse(65537, phi)
        m = pow(enc, d, n)
        print(long_to_bytes(m))

'''
r = remote('07.cr.yp.toc.tf', 22010)

r.interactive()
'''