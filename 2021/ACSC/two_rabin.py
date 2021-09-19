from Crypto.Cipher import AES, PKCS1_OAEP, PKCS1_v1_5
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import pad
from Crypto.Util.number import inverse, long_to_bytes, bytes_to_long, isPrime, getPrime
from sympy.matrices.matrices import num_mat_mul
from tqdm import tqdm
from pwn import *
from sage.all import *
import gmpy2, pickle, itertools, sys, json, hashlib, os, math, time, base64, binascii, string, re, struct, datetime, subprocess
import numpy as np
import random as rand
import multiprocessing as mp
from base64 import b64encode, b64decode
from sage.modules.free_module_integer import IntegerLattice
from ecdsa import ecdsa
from Crypto.Hash import SHA3_256, HMAC, BLAKE2s
from sage.modules.free_module_integer import IntegerLattice
from Crypto.Cipher import AES, ARC4, DES

flag1_len = 98
n = 105663510238670420757255989578978162666434740162415948750279893317701612062865075870926559751210244886747509597507458509604874043682717453885668881354391379276091832437791327382673554621542363370695590872213882821916016679451005257003326444660295787578301365987666679013861017982035560204259777436442969488099
B = 12408624070212894491872051808326026233625878902991556747856160971787460076467522269639429595067604541456868927539680514190186916845592948405088662144279471
c1 = 47149257341850631803344907793040624016460864394802627848277699824692112650262968210121452299581667376809654259561510658416826163949830223407035750286554940980726936799838074413937433800942520987785496915219844827204556044437125649495753599550708106983195864758161432571740109614959841908745488347057154186396
c2 = 38096143360064857625836039270668052307251843760085437365614169441559213241186400206703536344838144000472263634954875924378598171294646491844012132284477949793329427432803416979432652621257006572714223359085436237334735438682570204741205174909769464683299442221434350777366303691294099640097749346031264625862

flag2_len = 98
hard_c1 = 73091191827823774495468908722773206641492423784400072752465168109870542883199959598717050676487545742986091081315652284268136739187215026022065778742525832001516743913783423994796457270286069750481789982702001563824813913547627820131760747156379815528428547155422785084878636818919308472977926622234822351389
hard_c2 = 21303605284622657693928572452692917426184397648451262767916068031147685805357948196368866787751567262515163804299565902544134567172298465831142768549321228087238170761793574794991881327590118848547031077305045920819173332543516073028600540903504720606513570298252979409711977771956104783864344110894347670094

P = PolynomialRing(Zmod(n), 'x')
x = P.gen()


f = x * (x + B) - c1
mul = (1 << (8 * (128 - flag1_len)))
cc = bytes_to_long(b"\x1e" * 30)

g = (mul * x + cc) * (mul * x + cc + B) - c2
g = g.monic()

h = f - g 
cc = h.coefficients()

m = (int(cc[0]) * inverse(int(n - cc[1]), n)) % n
flag1 = long_to_bytes(m)

'''
from sage.matrix.matrix2 import Matrix 

def resultant(f1, f2, var):
    return Matrix.determinant(f1.sylvester_matrix(f2, var))

n = 105663510238670420757255989578978162666434740162415948750279893317701612062865075870926559751210244886747509597507458509604874043682717453885668881354391379276091832437791327382673554621542363370695590872213882821916016679451005257003326444660295787578301365987666679013861017982035560204259777436442969488099
B = 12408624070212894491872051808326026233625878902991556747856160971787460076467522269639429595067604541456868927539680514190186916845592948405088662144279471

flag2_len = 98
hard_c1 = 73091191827823774495468908722773206641492423784400072752465168109870542883199959598717050676487545742986091081315652284268136739187215026022065778742525832001516743913783423994796457270286069750481789982702001563824813913547627820131760747156379815528428547155422785084878636818919308472977926622234822351389
hard_c2 = 21303605284622657693928572452692917426184397648451262767916068031147685805357948196368866787751567262515163804299565902544134567172298465831142768549321228087238170761793574794991881327590118848547031077305045920819173332543516073028600540903504720606513570298252979409711977771956104783864344110894347670094



POL.<x, y> = PolynomialRing(Zmod(n))

f = x * (x + B) - hard_c1
g = (x + y) * (x + y + B) - hard_c2

res = resultant(f, g, x)
print(res)

POL.<y> = PolynomialRing(Zmod(n))
h = y^4 + 79890495413921998317755749042148232336863396932303122279875240130974185840791225375990895444267582903006871773965303045933569843994868097491212523442101173551279596449914721209311144221088483103651821516943100935730831208926818636117783500717523025942791406004609937226219367532136778920138824547343785869589*y^2 + 51092857055466673249380987427595244393604870491102664532822637562859699012127822437087645886784256843354629922356917208150074797607882719481678015312190222601448915412917964775219154717370030324105055787501129672958587186322761301111111401381772704665208028130495822463025972061040003730113313298834567354767

print(h.small_roots(X = (1 << 240), beta = 1.0, epsilon = 0.025))''


y_cands = [1637558660573652475698054766420163959191730746581158985657024969935597275, 105663510238670420757255989578978162666434740162415948750279893317701612062865075870926559751210244886747509597507458509604874043682717453885668881354391379276091832437791327382673554621542363370695590872213882821916016679451005257003324807101635213925825667932900258849901826251288979045274120411473033890824]

POL.<x> = PolynomialRing(Zmod(n))

for y in y_cands:
    f = x * (x + B) - hard_c1
    g = (x + y) * (x + y + B) - hard_c2
    h = f - g
    print(h)
    cc = h.coefficients()
    print(cc)
    x = - cc[0] / cc[1]
    print(h(x))
    x = int(x)
    print("result", x)
    print(int(x * (x + B) - hard_c1) % n)
    print(int((x+y)*(x+y+B)-hard_c2) % n)
    break


'''
x1 = 37412309942286574006158913496010620267687663146876352767622106656129986496651165862840203148321069273733293624726376167460944865534151793748073347584719705531628535234167400567407324714477822390166015938266208084466510307154956915004073076813624952897284616411776573796324151099101617608303133521659321079317
x1 = n - B - x1

print((x1 * (x1+ B) - hard_c1) % n)


m = x1 >> 240
flag2= long_to_bytes(m)
print(flag2)

print(flag1 + flag2)