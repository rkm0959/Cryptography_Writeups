# simplify polynomial in sage
p = 86160765871200393116432211865381287556448879131923154695356172713106176601077
b = 71198163834256441900788553646474983932569411761091772746766420811695841423780
m = 88219145192729480056743197897921789558305761774733086829638493717397473234815
w0 = 401052873479535541023317092941219339820731562526505
w1 = 994046339364774179650447057905749575131331863844814
 
nbits = 256
P.<x, y> = PolynomialRing(GF(p))
k = (nbits * 2 + 2) // 3
 
f = w0 * 2^(nbits - k) + x
g = w1 * 2^(nbits - k) + y
 
h = g - f^2 - b
print(h)
 
# python
 
def ceil(n, m):
    return (n + m - 1) // m
 
def optf(A, M, L, R):
    if L == 0:
        return 0
    if 2 * A > M:
        L, R = R, L
        A = M - A
        L = M - L
        R = M - R
    cc_1 = ceil(L, A)
    if A * cc_1 <= R:
        return cc_1
    cc_2 = optf(A - M % A, A, L % A, R % A)
    return ceil(L + M * cc_2, A)
 
x = 18867904637006146022735447
y = 19342813113834066795298816
p = 86160765871200393116432211865381287556448879131923154695356172713106176601077
b = 71198163834256441900788553646474983932569411761091772746766420811695841423780
m = 88219145192729480056743197897921789558305761774733086829638493717397473234815
w0 = 401052873479535541023317092941219339820731562526505
w1 = 994046339364774179650447057905749575131331863844814
 
C1 = 55130802749277213576496911760053178817655787149958046010477129311148596128757
C2 = 78083221913223461198494116323396529665894773452683783127339675579334647310194
 
nbits = 256
k = (nbits * 2 + 2) // 3
 
delt = nbits - k
# C1 x + y + C2 - x^2 == 0 mod p
# C1 x == x^2 - y - C2 mod p
 
L = (0 - (1 << (delt)) - C2 + p) % p
R = ((1 << (2 * delt)) - C2 + p) % p
 
lst = 0
while lst <= (1 << delt):
    NL = (L - C1 * (lst + 1)) % p
    NR = (R - C1 * (lst + 1)) % p
    if NL > NR:
        lst = lst + 1
    else:
        cc = optf(C1, p, NL, NR)
        lst = lst + 1 + cc
    mm = m
    x = lst
    v0 = w0 * (1 << (nbits - k)) + x
    v1 = (v0 * v0 + b) % p
    v = v1
    # try out!
    for i in range(5):
        v = (v * v + b) % p
        mm ^= v
    print(long_to_bytes(mm))
