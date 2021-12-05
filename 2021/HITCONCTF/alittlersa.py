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

n = 73105772487291349396254686006336120330504972930577005514215080357374112681944087577351379895224746578654018931799727417401425288595445982938270373091627341969888521509691373957711162258987876168607165960620322264335724067238920761042033944418867358083783317156429326797580005138985469248465425537931352359757
e = 4537482391838140758438394964043410950504913123892269886065999941390882950665896428937682918187777255481111874006714423664290939580653075257588603498124366669194458116324464062487897262881136123858890202346251370203490050314565294751740805575602781718282190046613532413038947173662685728922451632009556797931
enc = 14558936777299241791239306943800914301296723857812043136710252309211457210786844069103093229876701608756952780774067174377636161903673229776614350695222134040119114881027349864098519027057618922872932074441000483969146246381640236171500856974180238934543370727793393492372475990330143750179123498797867932379

p = GCD(n, pow(2, e - 1, n) - 1)
q = n // p 

d = inverse(e, (p - 1) * (q - 1))
print(long_to_bytes(pow(enc, d, n)))