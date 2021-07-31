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

def inthroot(a, n):
    if a < 0:
        return 0
    return a.nth_root(n, truncate_mode=True)[0]

def solve(n, phi):
    tot = n - phi + 1
    dif = inthroot(Integer(tot * tot - 4 * n), 2)
    dif = int(dif)
    p = (tot + dif) // 2
    q = (tot - dif) // 2
    if p * q == n:
        return p, q
    return None, None

e = 93546309251892226642049894791252717018125687269405277037147228107955818581561
n_1 = 36029694445217181240393229507657783589129565545215936055029374536597763899498239088343814109348783168014524786101104703066635008905663623795923908443470553241615761261684865762093341375627893251064284854550683090289244326428531870185742069661263695374185944997371146406463061296320874619629222702687248540071
n_2 = 29134539279166202870481433991757912690660276008269248696385264141132377632327390980628416297352239920763325399042209616477793917805265376055304289306413455729727703925501462290572634062308443398552450358737592917313872419229567573520052505381346160569747085965505651160232449527272950276802013654376796886259
enc_1 = 4813040476692112428960203236505134262932847510883271236506625270058300562795805807782456070685691385308836073520689109428865518252680199235110968732898751775587988437458034082901889466177544997152415874520654011643506344411457385571604433702808353149867689652828145581610443408094349456455069225005453663702
enc_2 = 2343495138227787186038297737188675404905958193034177306901338927852369293111504476511643406288086128052687530514221084370875813121224208277081997620232397406702129186720714924945365815390097094777447898550641598266559194167236350546060073098778187884380074317656022294673766005856076112637129916520217379601

c = continued_fraction(Integer(n_2) / Integer(n_1))

for i in range(144, 150):
    k = c.numerator(i)
    x = c.denominator(i)
    if GCD(e, k) != 1:
        continue
    res = inverse(e - k, e)
    cc = crt(res, 0, e, x)
    md = e * x // GCD(e, x)

    st = cc + (n_1 // md) * md - 100 * md
    for j in tqdm(range(200)):
        p, r = solve(n_1, st)
        if p != None and r != None:
            print(p)
            print(r)
            print(i)
        st += md


k = c.numerator(148)
x = c.denominator(148)

p = 7740199148476800803673451963952800996127342583838008667743568101487543296902409686375546874929891061046851187524614260725691579512099094584653349439579981
r = 4654879513314265302084692675411717211123457843532092691680754310965170424288171634994824679985917933617051111117318945995533396432809254742790610225117891

assert p * r == n_1
assert (r - 1) % x == 0

y = (r - 1) // x

d_1 = inverse(e, (p - 1) * (r - 1))
print(long_to_bytes(pow(enc_1, d_1, n_1)))