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
    return a.nth_root(n, truncate_mode=True)[0]

n = 4089970435799485944845994618559338051531582439055103221708293526218728906353918946098232625828564452708462506212931164865409431611945595415131998235807086659837640853295321598775515647861254598966969172678095439847663743911237641195098308362089595490018191770306216664723350055486605458160385345003417891944003478925394870548288214767072658414165479822695771789187019901630413113599342140268453122777430067666325912180274278137101383601326698480143821170735169310132840784184879141246991972503862326224250936845306516803720665441791796048334138363831242185281966539369780397034691030461876818316346943094892808137678842160570973321539661328404123273571021380772356250075380577582456290356333947267024198650423450369405882615317810372461002336352761355414418664414326630435306180894954623590850643538757425680940155491735581111015977603686922912160015090705453777238815496189845595915225749179028459977016669318750266681668851
p = 91972446512790925683956453962519352337632469173406379094130198034555959975569879415075613396254272160165235249030778177375943900978867753613715564995164505120442910050295445351490937558501759129394135990365315094309836981073373172874999494735660534601914289761655577005808392344519728050106723842026704809235495396150207276789570314980808119535274465657856735569619954972153418444487930499472404937326796989011183232821191262028342771966190429127133265943072339641806915516501187961449478296741202742771978611662563389667164338838353973160202396587739973519827967117491027727474337868960109652713113009278837371474307

for i in range(2, 80000):
    if p % i == 0:
        p = p // i
enc = 20315271527077432270996990845747698347338584488614632655532473484434569870503757346086410711370429356387090977849666434609702984664546419437584478588002664686362192960713045741684945264499978733638484342672874209663842461035266561002384621125370382377967902177239827007920419237867503049669915271334400478677169593999430085491092759981505056250395403682860468601069532823295441209489121524828875185807678032868596159060330837566781786590326665811555730760578502239498005000235490379690756693283420093049211557684207438979536818698929451366356394530375835945974079228171052177243605168798113254266730333626698300154036

q = n // p
p = inthroot(Integer(p), 2)
p = int(p)


phi = (p-1) * (q-1)
d = inverse(65537, phi)

m = pow(enc, d, p * q)

print(long_to_bytes(m))

'''
r = remote('04.cr.yp.toc.tf', 38010)

def read_lines(num = 5):
    for _ in range(num):
        r.recvline()

def get_enc(m):
    read_lines()
    r.sendline("E")
    r.recvline()
    r.sendline(str(m))
    cc = r.recvline().split()[-1]
    return int(cc)

def get_dec(m):
    read_lines()
    r.sendline("D")
    r.recvline()
    r.sendline(str(m))
    cc = r.recvline().split()[-1]
    return int(cc)

def get_flag():
    read_lines()
    r.sendline("S")
    cc = r.recvline().split()[-1]
    return int(cc)

read_lines()

B = get_enc(1 << 800)
T = get_enc(1 << 1600)

BB = get_enc(1 << 900)
TT = get_enc(1 << 1800)

n = GCD(B * B - T, BB * BB - TT)

for i in range(2, 80000):
    if n % i == 0:
        n = n // i

print(n)

G = get_dec(n-5)
GG = get_dec(n-3)

q = GCD(G * G + 5, GG * GG + 3)

print(q)

print(get_flag())
'''

