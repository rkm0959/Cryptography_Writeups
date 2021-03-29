pytp = 13046889097521646369087469608188552207167764240347195472002158820809408567610092324592843361428437763328630003678802379234688335664907752858268976392979073
a = 10043619664651911066883029686766120169131919507076163314397915307085965058341170072938120477911396027902856306859830431800181085603701181775623189478719241
b = 12964455266041997431902182249246681423017590093048617091076729201020090112909200442573801636087298080179764338147888667898243288442212586190171993932442177
 
E = EllipticCurve(GF(p),[a,b])
 
G = E(11283606203023552880751516189906896934892241360923251780689387054183187410315259518723242477593131979010442607035913952477781391707487688691661703618439980, 12748862750577419812619234165922125135009793011470953429653398381275403229335519006908182956425430354120606424111151410237675942385465833703061487938776991)
u = G[0]
v = G[1]
 
N = 22607234899418506929126001268361871457071114354768385952661316782742548112938224795906631400222949082488044126564531809419277303594848211922000498018284382244900831520857366772119155202621331079644609558409672584261968029536525583401488106146231216232578818115404806474812984250682928141729397248414221861387
c = 15850849981973267982600456876579257471708532525108633915715902825196241000151529259632177065183069032967782114646012018721535909022877307131272587379284451827627191021621449090672315265556221217089055578013603281682705976215360078119427612168005716370941190233189775697324558168779779919848728188151630185987
 
P.<x, y> = PolynomialRing(GF(p))
f = y ** 2 - x ** 3 - a * x - b
g = x * ((y - v) * (y - v)  - (x + u) * (x-u) * (x-u)) - N * (x-u) * (x-u)
 
print(g.monomials())
# [x^4, x^3, xy^2, x^2, xy, x, 1]
 
T = g.coefficients()
P.<x> = PolynomialRing(Zmod(p))
f = 0
g = 0
f += T[0] * x^4
f += T[1] * x^3 
f += T[2] * x * (x^3 + a* x + b)
f += T[3] * x^2 
f += T[5] * x
f += T[6]
 
g += T[4] * T[4] * x^2 * (x^3 + a*x + b)
 
 
h = f * f - g 
 
print(h.roots())
 
N = 22607234899418506929126001268361871457071114354768385952661316782742548112938224795906631400222949082488044126564531809419277303594848211922000498018284382244900831520857366772119155202621331079644609558409672584261968029536525583401488106146231216232578818115404806474812984250682928141729397248414221861387
c = 15850849981973267982600456876579257471708532525108633915715902825196241000151529259632177065183069032967782114646012018721535909022877307131272587379284451827627191021621449090672315265556221217089055578013603281682705976215360078119427612168005716370941190233189775697324558168779779919848728188151630185987
 
# cand = h.roots()
cand = [(5266647903652352665309561331835186152327627163271331811555419978564191000470060566535428497675116887002541568904535904345037425011015457585262022604897451, 1), (4292528248136861387890911319917455946841411872473250675409509735620572311636407361858881556677385609500178629430025710517411214702704597103005396234440737, 1), (11283606203023552880751516189906896934892241360923251780689387054183187410315259518723242477593131979010442607035913952477781391707487688691661703618439980, 2)]
 
for p, t in cand:
    q = N // p
    phi = (p-1) * (q-1)
    print(p * q - N)
    d = inverse(65537, phi)
    print(long_to_bytes(pow(c, d, N)))