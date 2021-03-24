def rhexc():
    t = random.randrange(0, 16)
    if t <= 9:
        return chr(ord('0') + t)
    if t >= 10:
        return chr(ord('a') + t - 10)
 
conn.recvline()
msgs = []
h = []
r1 = []
r2 = []
s = []
for i in range(0, 10):
    conn.recvline()
    conn.recvline()
    conn.recvline()
    conn.recvline()
    conn.recvline()
    conn.send("S\n")
    conn.recvline()
    msg = rhexc() + rhexc() + rhexc() + rhexc()
    msgs.append(bytes.fromhex(msg))
    hh = int(hashlib.sha384(bytes.fromhex(msg)).hexdigest(), 16)
    h.append(hh)
    conn.send(msg + "\n")
    T = conn.recvline().split()
    r1.append(int(T[0].decode()))
    r2.append(int(T[1].decode()))
    s.append(int(T[2].decode()))
 
f = open("data.txt", "w")
 
def goprint(t, s):
    f.write(s + " = [")
    for i in range(len(t)):
        f.write(str(t[i]))
        if i != len(t) - 1:
            f.write(", ")
    f.write("]")
 
goprint(h, "h")
f.write("\n")
goprint(r1, "r1")
f.write("\n")
goprint(r2, "r2")
f.write("\n")
goprint(s, "s")
f.write("\n")
f.close()
print("DONE")
 
a = int(input())
b = int(input())
c = int(input())
 
conn.recvline()
conn.recvline()
conn.recvline()
conn.recvline()
conn.recvline()

# sage
import hashlib
import random
 
def Babai_closest_vector(M, G, target):
        small = target
        for _ in range(1):
            for i in reversed(range(M.nrows())):
                c = ((small * G[i]) / (G[i] * G[i])).round()
                small -=  M[i] * c
        return target - small  
 
def sign(msg, d):
    x = int(hashlib.sha1(int.to_bytes((int)(d), 48, byteorder='big')).hexdigest(), 16) % 2**25
    while True:
        k1 = (random.getrandbits(340) << 25) + x
        k2 = (random.getrandbits(340) << 25) + x
        r1 = (k1*G).xy()[0]
        r1 = (int)(r1)
        r2 = (k2*G).xy()[1]
        r2 = (int)(r2)
        if r1 != 0 or r2 != 0:
            break
    r1 = (int)(r1)
    r2 = (int)(r2)
    d = (int)(d)
    h = int(hashlib.sha384(msg).hexdigest(), 16)
    s = ((int)(inverse_mod(k1, n)*(h*r1 - r2*d))) % n
    return (r1, r2, s)
 
p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFFFF0000000000000000FFFFFFFF
E = EllipticCurve(GF(p), [-3, 0xB3312FA7E23EE7E4988E056BE3F82D19181D9C6EFE8141120314088F5013875AC656398D8A2ED19D2A85C8EDD3EC2AEF])
n = 39402006196394479212279040100143613805079739270465446667946905279627659399113263569398956308152294913554433653942643
G = E(0xaa87ca22be8b05378eb1c71ef320ad746e1d3b628ba79b9859f741e082542a385502f25dbf55296c3a545e3872760ab7, 0x3617de4a96262c6f5d9e98bf9292dc29f8f41dbd289a147ce9da3113b5f0b8c00a60b1ce1d7e819d7a431d7c90ea0e5f)
 
M = Matrix(ZZ, 10, 10)
 
h = [233731106310751937192664573894149799156520678027609284447669359448796436322955092470459836110792934841120158122984, 24811003402020297682803985280385324059294547276381651936828219428316450314628727089306406877936309521585868406250470, 17531688510937980482168807263229017380075873963160377208275450719528636667269895679466032893594537651522283322716674, 36047996617843056294579056584530136441992332560008111725661742840889647330983212663288175229441011598065500536724651, 11272134849660563344197668625651398585469230739650422640053316031881717853156318362750855003467577550566014131759397, 12921752283394782997197083154961040846567875585176615600282439213271258534634490795163442206145433928804694064497184, 23550485659661088231333360400047313315118168135461773986636400711616230052409480901284050511344421804458290935165361, 28496735302713412781192449440072502796901684384799422985608472930590031587697602766375490458840116389733463012282962, 8277886329528032187549731002807594806536689677333903394331300955320330584538612138873925253500020691928232999586476, 15008843981182040291480007346492436282071178418873478338505839724866567471088415321631607204728733513138973751666571]
r1 = [12579209808189312915327132001276994446255172328500500695944989889711062858983163741271309992272077550124869505655381, 751327735728556148057917754296484320013694567443429719964844556884059843931387861716234725405209534287623519155458, 5371112946404190387697534646035651694165960225187891433236446686273017304702714837212569297073575677253044266881569, 331352105137929972597744016411888049220372925675806096677491319577734959841100142754252499792455324441192018313181, 7888617807239874165986404317109270600428296541740743307263264541916487472897668559357227416927514439026859501878365, 27761407228814320863611585879580881526756177120011066949498954824121650008685326439038329973891388684478285112725357, 27729723957967183136564649593980227227433733353902657860894937180736101915856597513173881921545820999053402276812094, 7364956988030862701298496872632133592704536625686657579967644830046483396779789062671782387408609718000755429523017, 37812330351370334405023218191363149079167490389863184907107776623417575732769914373075308521813667861691959707092667, 2624169019517838564518311384425555195298893854856387163253094963173848316296091845329567038393753791750586302201087]
r2 = [3362705797849617878647365660985990566049333116696565173083098561696239463413527201559140422082923583525045722549763, 14145060354523589059216194767137578723898667342472872089321140612118830294396552192914912108964170720929305735415873, 29896158881994803685845271456929722092964179790028911234436030397936425532648870182944208462169501559557896423331008, 28295713529327846754165290558634286334350103809603649440117629677663367232344783261643275422157945835517134018581552, 9832320742110221576843735934134914437015558355201552824473334305115758409450236891997901207964296770834208882940712, 4863643686082209193655332852839008988042953344444353171052414901807831698624799620686397115822220675031235649084871, 2172376087957939144239533590664428657297700738539681962241559027660276255529486815550264413927604748955534219627695, 39270978975994145259001854586943865848306851245548202584185719889584304215280317078715908462808066433518126930812549, 34215025679986052889776564064620447574359162481440315252719789122933592974697130074626618888824626087631554900691781, 31458354800313627611820028529141092961133175220661883156536844963568120403379640053999048076879854251402929920752081]
s = [17925111440396892739033187521377597454621431410987251376820936783063824269472232155851393375468659283009982667848669, 21853582586273412881491430100511011448648027948649700911052731210656190304335253416414001734385549707694334614279337, 19106220304410988776781688031238993716481941836023244437887325024470240140203226637806963202138139801315239237169074, 17507801404065436507268995586301878815717284846882572361951752925726533505019428040074124887812030279468394962880645, 4900819118697444872055280551871388610242725910301521205805242844252676607768719405815620318563132591329844695620900, 28480294438694078949495111903243339194235498093230054160772397254022021764455096010558032230371482379081669589216030, 25703610354773191595397225912857234424274497331129500961893925842562869928957637655440191485239263057624366236967535, 25089230670220425716164780435793841951903552099807404714502656133071929486670807789632806166532377757560189053522629, 38581148690570764731827681277745747604768765690301001244659037510529992367464486509918486337349511386868684709829501, 33302053638667654050592244700225839457979855163938098516151926858754963517053234739223403629384061080926568390283532]
 
iv = inverse_mod(2 ** 25, n)
 
for i in range(0, 9):
    M[0, i] = (((inverse_mod(s[i+1], n) * r2[i+1] - inverse_mod(s[0], n) * r2[0]) * iv) % n) * n
    M[i+1, i] = n * n
M[0, 9] = 1
 
Target = [0] * 10
for i in range(0, 9):
    Target[i] = (((inverse_mod(s[i+1], n) * r1[i+1] * h[i+1] - inverse_mod(s[0], n) * r1[0] * h[0]) * iv) % n) * n
Target[9] = 2 ** 383
 
M = M.LLL()
GG = M.gram_schmidt()[0]
Target = vector(Target)
TT = Babai_closest_vector(M, GG, Target)
print(TT[9]) ## d
 
sec = b'I know alll of your secrets!'
X = sign(sec, TT[9])
print(X[0])
print(X[1])
print(X[2])