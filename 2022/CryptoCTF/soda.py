from sage.all import * 
from Crypto.Util.number import long_to_bytes, bytes_to_long, isPrime, inverse, getPrime
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from pwn import * 
import random as rand
from tqdm import tqdm
import requests


conn = remote("01.cr.yp.toc.tf", 37711)
conn.interactive()
'''
n = 99079213864225638211164004707660376360561061293868813414340853792016960003532290684350987975057143145176307506763351191420928302748101383361521210974297633813257059844605439910514985971362362677843666944971712543939026392257685421348762705964915220795881554670574231326045740084163983602187913327355090728057
g = 31337

CRY = "Long Live Crypto :))"
m = bytes_to_long(CRY.encode('utf-8'))

e = 2 * (pow(g, m**2, n) % 2**152) ^ 1

print(e)

f = 5500056052324938008435708454209
247166830528795
print(e // f)
# g^(1/d) g^(1/e)

# x/d + y/e = 1/de
# xe + yd = 1
'''

n = 99079213864225638211164004707660376360561061293868813414340853792016960003532290684350987975057143145176307506763351191420928302748101383361521210974297633813257059844605439910514985971362362677843666944971712543939026392257685421348762705964915220795881554670574231326045740084163983602187913327355090728057
g = 31337

e1 = 5500056052324938008435708454209
e2 = 1594624713089
e3 = 31
e4 = 5

es = [e1, e2, e3, e4]

v1 = 362776415939282391995369925305672886950547675685444295484110987110488521011703056112801706241313730036911714423526013913063907531694916777197571318060499009170751721426441702120029722826383427505418005416177887491742275282458338400259266013812704073894098052310137320527191768918236482180566662073579941699
v2 = 12173929951841424182184063376135073788443240450423036672109749907952244392110996949324143486003152701082755690539080043261103258782325926735857186296215061109149081729361930541564286661730667986827674200598068432999248950045634992380653532549535898984125610975140289035006339521005757187026750502924543286738
v3 = 15519540555078928391030899917238810790284404295915549220239255649963231007150180386051477327381780633175305184952799995790973884138786516230413188680870612458393718201400853694829470863781241366810492309759420205352989073800749245520253140011280703996490405806018679523166997064800848746771999478069900757915
v4 = 56136745883418672819963957794553337393873622983135649464002964869418303480198570763259743615712081535614402003570073358902688258614065597765240998310251213653863073713130938860583181140723020764809984746061751625650085857702351300061362207024264831308739398139705320188072142210413215250031359631939388461017

vs = [v1, v2, v3, v4]

# a e2e3e4 + b e3e4e1 + c e4e1e2 + d e1e2e3 = 1

a = inverse(e2*e3*e4, e1)
b = inverse(e3*e4*e1, e2)
c = inverse(e4*e1*e2, e3)
d = - (1 - a * e2 * e3 * e4 - b * e3 * e4 * e1 - c * e4 * e1 * e2) // (e1 * e2 * e3)

fin = 1
fin = fin * pow(v1, a, n)
fin = fin * pow(v2, b, n)
fin = fin * pow(v3, c, n)
fin = fin * inverse(pow(v4, d, n), n)

print(fin)

CRY = "Long Live Crypto :))"
m = bytes_to_long(CRY.encode('utf-8'))
e = 2 * (pow(g, m**2, n) % 2**152) ^ 1

print(pow(fin, e, n))

# xe2 + ye1 = 1