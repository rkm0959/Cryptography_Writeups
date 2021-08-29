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
m = bytes_to_long(flag)

e = 65537

n = p * q
  = 40246250034008312612597372763167482121403594640959033279625274444300931999548988739160328671767018778652394885185401059130887869211330599272113849088780129624581674441314938139267245340401649784020787977993123159165051168187958742107

d = 0b1[REDACTED]00001101110000010101000000101110000111101011011101111111000011110101111000100001011100001111011000010101010010111100000011000101000001110001111100001011001100010001100000011100001101101100011101000001010001100000101000001

c = pow(x**2 + m + y, e, n)
  = 28505561807082805875299833176536442119874596699006698476186799206821274572541984841039970225569714867243464764627070206533293573878039612127495688810559746369298640670292301881186317254368892594525084237214035763200412059090430060075

x**2 * (y - 146700196613209180651680280746469710064760660116352037627587109421827052580531) + y**2 * (x - 146700196613209180651680280746469710064760660116352037627587109421827052580531) = 27617741006445293346871979669264566397938197906017433294384347969002810245774095080855953181508639433683134768646569379922750075630984038851158577517435997971553106764846655038664493024213691627948571214899362078353364358736447296943
'''

def inthroot(a, n):
    return a.nth_root(n, truncate_mode=True)[0]

n = 40246250034008312612597372763167482121403594640959033279625274444300931999548988739160328671767018778652394885185401059130887869211330599272113849088780129624581674441314938139267245340401649784020787977993123159165051168187958742107

a = 146700196613209180651680280746469710064760660116352037627587109421827052580531
b = 27617741006445293346871979669264566397938197906017433294384347969002810245774095080855953181508639433683134768646569379922750075630984038851158577517435997971553106764846655038664493024213691627948571214899362078353364358736447296943

assert n == 4 * a * a * a + b

# x^2(y-a) + y^2(x-a) = b
# xy(x+y) - ax^2 - ay^2 = b
# uv - a(u^2 - 2v) = b
# (u + 2a) v = au^2 + b
# v = (au^2 + b) / (u + 2a)
# (u + 2a)(au - 2a^2)
# v = au - 2a^2 + (4a^3 + b) / (u + 2a)
# (x+a)(y+a) = a(x+y+2a) - 2a^2 + (4a^3 + b) / (x + y + 4a)
# (x+a)^2y + (y+a)^2 x = b


# from rbtree's code with partial exposure attack on d
p = 893797203302975694226187727100454198719976283557332511256329145998133198406753
q = n // p

u = p - 2 * a
v = (a * u * u + b) // (u + 2 * a)
dif = inthroot(Integer(u * u - 4 * v), 2)

x = (u + dif) // 2
y = (u - dif) // 2

e = 65537 

c = 28505561807082805875299833176536442119874596699006698476186799206821274572541984841039970225569714867243464764627070206533293573878039612127495688810559746369298640670292301881186317254368892594525084237214035763200412059090430060075

d = inverse(e, (p-1) * (q-1))

res = pow(c, d, n)

print(long_to_bytes(res - x * x - y))
print(long_to_bytes(res - y * y - x))
