## kth root of n, (integer rounded) using binary search
def kthp(n, k):
    lef = 1
    rig = 2
    while rig ** k < n:
        rig = rig << 1
    while lef <= rig:
        mid = (lef + rig) // 2
        if mid ** k >= n:
            best = mid
            rig = mid - 1
        else:
            lef = mid + 1
    return best        
 
hint = 49380072119923666878249192613131592074839617141388577115293351423167399196342955381916004805107462372075198711094652660372962743330048982663144511583693085794844754920667876917018671057410534100394910738732436580386544489904637
D = 15515568475732467854453889
n = 6337195756161323755030821007055513472030952196189528055855325889406457327105118920711415415264657259037549360570438684177448730672113983949019501534456306880443480045757556693491657382839313528872206247714019569057234809244745178637139314783799705976807860096251357543835678457306901513720623505353691449216464755029227364954566851544050983088509816181294050114090489118245225264446360947782705558298586215673137402419393055466097552149369002210996708260599901728735979196557443301850639382966378922196935480476418239903494619475397129088135961432456212959427154766737697387874383258702208776154403167756944619240167487825357079536617150547060929824469887270443261440975473300946304087345552321787097829023298865763114083681766490064879774973163395320826072815425507105417077348332650202626344592023021273
 
## hint / D <= sqrt(p) + sqrt(q) <= (hint + 1) / D
X = (hint * hint) // (D * D) - 2 * kthp(n, 2)
Y = (hint * hint + 2 * hint + 1) // (D * D) - 2 * kthp(n, 2)
X = int(X)
Y = int(Y)
## small p + q = Y
lr = (X + kthp(X * X - 4 * n, 2)) // 2
sm = (Y + kthp(Y * Y - 4 * n, 2)) // 2
 
sm = int(sm)
lr = int(lr)
df = sm-lr
assert df >= 0
print((int)(df).bit_length())
 
K = Zmod(n)
P.<x> = PolynomialRing(K, implementation='NTL')
f = x + lr
 
T = f.small_roots(X = 2**600, beta=0.5, epsilon = 0.02)
print(T) ## T[0] + lr is a factor of n
 
for x in c:
    if pow(x, (p-1) // 2, p) == 1 and pow(x, (q-1) // 2, q) == 1:
        s += '1'
    else:
        s += '0'
 
s = int(s, 2)
print(long_to_bytes(s))