
n = 990853953648382437503731888872568785013804329239290721076418541795771569507440261620612308640652961121590348037236708702361580700250705591203587939980126323233833431892076634892318387020242015741789265095380967467201291693288654956012435416445991341222221539511583706970342630678909437274145759598920314784293470918464283814408418704426938549136143925649863711450268227592032494660523680280136089617838412326902639568680941504799777445608524961048789627301462833

sqs_x = 1001889042584622165096707162820969641261936518606114932283449833689842605494232162233427308149110206898774648323901197584988800544298767207498917489687760348893066165770330003666171064100313336857858415515517459327070576132818136847851164947456554762351786514776996422591655635049692973362933421324374645146066084796640281391820922033230738243001209452415713381857478289981662189358380124498996289558936053629792996741417765705622086006316959540108916072112293778
sqs_y = 8781469273786878043468495164317015078264847393480801720785812953432039337962883984037802654070395366773608241459429886746526651070929117977012569276548013097453880075033234730789796909481124141747886397002903693276754049295450102033564713634120853609285252645689441580785059562939555162102574895709558892933580665857142607645744221115675565509256842129041293633289117994102151597073488

val1 = 556954597890718089562648176164739639586460307752267454805298192848605615366579150030483799006827103535339142717932306928770484680076860001562810433899885890069005680801575405309740776592406200525131070248411928503884713972938287798169613600964772210781998646396459889163196473220992093288779913832197120352036941346880882091145029145598473066832550203137569747164571927772122555005549845150031028651760247238011835530863900

val2 =2913393110977130229215594407761176326994370363447666944838691033967613566692736514981906023253728095202953701890764569813524196322079382566815761215309133342812098500371337564471003505260943929533212002228893310223835505579536815670216817443903165990962459858508811589809252865913433564970873384535839549668760636659970086080058212782385461061203400476077693523581790440929401948075811464324561508632951257340083867258578892


p = random_prime(1 << 1024)

PR.<x> = PolynomialRing(GF(p))

def reduction(F):
    ret = 0
    tt = F.monomials()
    vals = F.coefficients()
    for i in range(len(tt)):
        ret += (x ** (tt[i].degree())) * vals[i]
    return ret

x1, x2, y1, y2 = GF(p)['x1,x2,y1,y2'].gens()

e = 111578009802636409437123757591617048189760145423552421418627338749835916561801

F1 = x1 * x1 + x2 * x2 - sqs_x 
F2 = y1 * y1 + y2 * y2 - sqs_y 
F3 = x1 * y1 + x2 * y2 - val1 
F4 = x1 * y2 - x2 * y1 - val2 

F5 = x1 * x1 + e * y1 * y1 - n 
F6 = x2 * x2 + e * y2 * y2 - n 

I = ideal(F1, F2, F3, F4, F5, F6)

vars = [x1, y1, x2, y2]

resultants = [F1, F2, F3, F4, F5, F6]

from tqdm import tqdm 

for i in tqdm(range(3)):
    new_resultants = []
    for j in range(1, len(resultants)):
        cc = resultants[0].sylvester_matrix(resultants[j], vars[i]).determinant()
        new_resultants.append(cc)
    resultants = new_resultants


print(resultants)

def isPowerOf2(T):
    tt, isok = Integer(T).nth_root(2, truncate_mode=True)
    if isok:
        return tt
    else:
        return -1

pol = reduction(resultants[1])
for true_y2, ex in pol.roots():
    true_y2 = int(true_y2)
    try:
        x2_sq = n - e * true_y2 * true_y2 
        x1_sq = sqs_x - x2_sq 
        y1_sq = sqs_y - true_y2 * true_y2 
        
        true_x1 = isPowerOf2(x1_sq)
        true_y1 = isPowerOf2(y1_sq)
        true_x2 = isPowerOf2(x2_sq)

        if true_x1 != -1 and true_y1 != -1 and true_x2 != -1:
            print(true_x1)
            print(true_y1)
            print(true_x2)
            print(true_y2)
    except:
        pass
