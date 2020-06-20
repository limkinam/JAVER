import requests
from bs4 import BeautifulSoup
import pymysql
conn = pymysql.connect(host='localhost',port=3306,user='root', password='ssafy',
                       db='javer', charset='utf8')
curs = conn.cursor()

sqldel = "delete from stock;"
curs.execute(sqldel)


# company_code를 입력받아 bs_obj를 출력
def get_bs_obj(company_code):
    url = "https://finance.naver.com/item/main.nhn?code="+ company_code
    result = requests.get(url)
    bs_obj = BeautifulSoup(result.content, "html.parser")
    return bs_obj


# company_code를 입력받아 now_price를 출력
def get_price(company_code):
    bs_obj = get_bs_obj(company_code)

    company_name = bs_obj.find("div",{"class":"wrap_company"})
    company_name_h2 = company_name.find("h2")
    co_name = company_name_h2.text

    no_today = bs_obj.find("p", {"class": "no_today"})
    blind = no_today.find("span", {"class": "blind"})
    now_price = int(blind.text.replace(",",""))


    # close 종가(전일)
    td_first = bs_obj.find("td", {"class": "first"})  # 태그 td, 속성값 first 찾기
    blind = td_first.find("span", {"class": "blind"})  # 태그 span, 속성값 blind 찾기
    close = int(blind.text.replace(",",""))

    # high 고가
    table = bs_obj.find("table", {"class": "no_info"})  # 태그 table, 속성값 no_info 찾기
    trs = table.find_all("tr")  # tr을 list로 []
    first_tr = trs[0]  # 첫 번째 tr 지정
    tds = first_tr.find_all("td")  # 첫 번째 tr 안에서 td를 list로
    second_tds = tds[1]  # 두 번째 td 지정
    high = int(second_tds.find("span", {"class": "blind"}).text.replace(",",""))

    # open 시가
    second_tr = trs[1]  # 두 번째 tr 지정
    tds_second_tr = second_tr.find_all("td")  # 두 번째 tr 안에서 td를 list로
    first_td_in_second_tr = tds_second_tr[0]  # 첫 번째 td 지정
    open = int(first_td_in_second_tr.find("span", {"class": "blind"}).text.replace(",",""))
    
    # low 저가
    second_td_in_second_tr = tds_second_tr[1]  # 두 번째 td 지정
    low = int(second_td_in_second_tr.find("span", {"class": "blind"}).text.replace(",",""))

    # 전일대비
    beforenum = int(now_price - close)

    sql = "insert into stock(name,now,befnum,close,high,open,low) values(%s,%s,%s,%s,%s,%s,%s)"

    curs.execute(sql, (co_name, now_price, beforenum, close, high, open, low))

    return co_name, now_price, beforenum, close, high, open, low

"""
    
    
    """


"""
셀트리온헬스케어 091990 / 에이치 엘비 028300 / CJ ENM 035760 / 스튜디오드래곤 253450 / 펄어비스 263750
케이엠더블유 032500 / 메디톡스 086900 / 휴젤 145020 / 원익IPS 240810 / 헬릭스미스 084990 /솔브레인036830 /SK머티리얼즈036490 /파라다이스034230
메지온140410 / 에스에프에이056190 / 아이티엠반도체084850 / 셀트리온제약068760 / 에코프로비엠247540 / 컴투스078340 / 젬백스082270

"""

company_codes = ["091990", "028300", "035760", "253450", "263750", "032500" ,"086900", "145020" ,"240810", "084990","036830","036490","034230","140410","056190","084850","068760","247540","078340","082270"]
test = ["065370","342550","341160","340440","311690","062970","327260","339950","340120","288330","336570","235980","340360","226330","322510","124560","335870","302550","337450","335890","290510","336060","278650","321550","297090","103840","190650","306040","216080","214260","084850","333430","279600","332710","333050","322180","331520","317530","272110","317870","318010","300120","158430","234690","332290","331380","330990","244460","317120","320000","256150","329560","311390","195500","328380","286750","317830","228670","186230","282880","317330","317770","318000","148150","313760","317850","241840","300080","323210","234340","289010","251970","312610","323280","323940","323230","293780","308100","305090","322780","321260","253840","307930","319660","319400","950180","317320","317240","125210","228760","317030","099750","313750","100790","247540","299660","278280","246960","104620","053580","238200","311270","310840","263050","290550","307180","310200","309930","299900","310870","307750","298380","100590","110020","270870","307870","302430","307070","290120","307280","128540","299910","900340","307160","111710","179290","117730","290660","246710","263690","217330","027360","208340","263020","227100","194700","268600","290670","285490","290650","306620","108490","153710","288620","293580","290720","110790","299170","219750","257370","291230","197140","303030","290740","173130","089970","086820","290380","110990","275630","290270","080720","204020","297570","226950","175250","289080","245620","284620","037030","016790","258830","122310","291210","287410","950170","253590","263700","064510","277070","226400","183490","006620","154030","260660","042000","219420","267790","255220","264660","269620","281410","187870","281740","260930","241770","234300","066360","007680","138580","279410","253450","276920","148140","950160","265560","234100","277480","263810","255440","277410","263920","243840","179900","171090","259630","174900","263540","263750","256940","263600","258610","270520","140670","900310","273060","118990","263800","263860","263720","091990","181340","271740","238490","251630","227610","272290","003380","261200","267320","250000","267980","225190","264850","161580","256630","166090","258790","251370","265520","263770","063760","264450","178320","183300","246720","217480","002800","083500","087260","241820","140070","206650","256840","195440","241520","246690","147760","204990","196300","203450","215600","254120","241790","220100","144960","156100","176440","220180","237880","900300","238120","252500","216050","239610","241710","900290","900280","189300","072990","950140","238090","050960","201490","250930","241690","250060","242040","234920","900270","230360","038160","208860","073560","123010","174880","071460","142760","237750","900260","144510","237690","148250","239340","243070","240810","228850","225330","228340","222110","211270","230980","115180","065660","236200","226350","142210","900250","221610","109610","224060","232140","191410","223310","145020","222980","206560","013310","217730","047920","133750","225530","140860","230240","122640","222040","058110","217820","213090","221840","197210","180400","127160","221980","212560","227950","214370","185490","190510","056090","226340","115960","182400","092870","226360","214870","225430","226440","225590","225570","217190","219130","175140","222080","220630","224110","196700","131760","222810","222800","189980","222420","094360","127710","214430","067730","220260","214450","219550","087010","218410","094170","214180","178780","160600","217600","166480","214310","177350","217270","218150","160980","217500","087600","217620","187420","215380","215480","215790","215360","215200","215090","215100","214680","195990","215000","214150","214270","189690","213420","060480","206640","208640","193250","204630","200470","200670","208710","189860","067390","080580","208350","160550","124500","142280","187220","208370","208140","149980","084650","200710","200780","207760","196170","206400","178920","140520","173940","205470","200230","194510","204840","204620","196490","205500","205100","191420","192440","182690","143540","203650","041920","194480","203690","192410","198440","187270","177830","090410","004650","192390","059120","200130","105550","196450","071850","187790","192250","138080","108790","053300","154040","090850","184230","049080","150840","085810","170030","067570","134580","182360","171120","171010","161570","138360","076610","168330","131970","150900","170920","119850","092040","130500","170790","151860","089600","950130","141080","158310","097800","104540","159580","114810","153490","099190","141020","159910","950110","046970","113810","141070","155650","149950","121850","149940","151910","097520","153460","106520","137400","141000","072950","143240","126870","147830","091590","140410","104830","127120","130580","131090","100660","115480","123260","139670","121800","112240","138070","123570","122870","136510","089530","089030","101240","007820","115530","043290","090360","131220","131390","143160","134780","137950","040910","123330","139050","089980","138610","109080","108380","019770","137940","131100","138690","122450","121440","136540","136480","134060","104480","008470","121600","093320","130740","131180","061970","126880","033560","048530","119860","131370","064290","131290","131400","120240","128660","131030","096690","033830","033170","122800","041460","105740","126600","123420","111870","123860","058400","069140","119830","101930","078650","068940","123840","117670","119500","068240","096530","122990","126700","126640","123410","123040","067920","119610","106190","114120","121890","123750","089850","111820","046120","070300","108320","079970","071200","100030","122690","900110","900100","115500","900120","115450","122350","115610","115310","106080","101330","114570","115570","115440","050860","114630","080530","900070","099520","114450","104460","096640","112040","108860","900080","088290","114190","115160","109960","099410","101000","109820","082920","042520","104200","052860","105330","109740","095700","108230","100130","103230","063080","109860","102120","101730","900040","102710","099440","102210","099220","101680","010240","101170","081150","098660","071670","101490","100120","102940","101400","106240","086890","104040","078070","086900","058630","059100","067630","092130","100700","098120","083470","100090","101390","076080","101670","094840","063170","047560","096240","101160","099320","064480","098460","067000","018620","095610","053280","096870","059210","097870","087730","091440","096040","097780","096630","068330","093920","067010","096350","069920","096610","092070","094820","086670","094190","095190","092300","093640","095910","081580","073110","094970","080520","095340","085910","095500","027580","086040","090740","057540","094940","095270","093190","091340","072770","094480","086520","065150","078340","095660","092600","069410","093380","086450","064820","091580","092460","073540","091120","094850","094860","078020","093520","048260","091970","092730","090460","039200","089010","090470","088130","084110","089150","091700","086390","090710","060540","066310","067280","086250","089890","080470","089140","089790","090150","088390","089230","043150","086960","038060","083660","062860","063570","086980","068050","085370","039290","078860","088910","054950","084730","086060","022220","088800","068760","083450","019990","079370","046110","085670","084370","083790","064550","084990","083640","085660","078140","067900","083550","084180","050540","080420","083650","079190","045890","082800","043910","079000","041020","078590","038070","079940","077360","083930","067310","082660","083310","080010","058220","078160","082850","080160","078890","050890","082210","082270","075130","080440","073490","079950","079960","080220","079170","079810","080000","052220","079650","052900","066910","049950","052460","072870","073010","046440","078600","054450","078150","067990","051360","072520","078130","068790","078940","048870","065350","039340","064260","011080","050090","029960","057030","065770","074430","066700","066900","078350","075970","069540","073190","054090","041910","073070","039670","067770","070590","073570","073640","065680","057880","060570","066410","067160","074600","071280","041440","069510","067170","054780","072020","065510","072470","068930","069110","069330","064760","052710","065950","047310","056000","041520","065560","064240","066790","069080","067080","066590","067290","066130","046140","065450","065130","065440","049630","021650","051370","065650","065570","066980","016100","065940","042040","066970","066670","066430","047820","064090","049960","053290","064520","035600","065170","034230","041590","042600","065500","060900","066620","065420","052770","064800","039980","048410","058610","045340","065710","065690","066110","043710","060560","036010","060280","065620","060230","057680","046940","060150","065530","063440","051160","065060","049180","060720","061040","050760","054210","050120","054410","060310","061250","053980","054050","039420","039440","049550","054670","060590","049070","060370","051380","053660","053270","034950","060260","060380","046310","058530","049720","052670","046890","013990","058450","059090","050320","054930","035200","054040","048470","060300","042500","058420","040350","054300","054340","047080","060250","053260","060240","056730","057500","041930","054220","014940","043590","058470","045300","056190","056700","054940","043370","054620","056360","043260","038340","051390","054540","053350","054630","056080","044490","053950","053700","054920","041960","053160","052400","054180","049470","053050","043090","053110","054800","047770","053800","040300","058820","035900","053590","021320","053060","053610","052790","053450","053030","052420","053620","052300","049520","048910","051980","051500","049120","043360","052330","052600","052020","043220","033790","051780","052190","051490","038870","045660","052260","045390","050110","036540","038500","048550","049830","044060","024850","048770","049430","044480","046390","014620","048430","017480","049480","036670","042510","039830","036190","046070","041830","014570","045520","022100","033600","044180","044960","032080","010470","044340","042940","048830","000250","044780","045510","045100","040160","043340","043650","037950","039030","038540","018680","039860","046210","045060","043100","042370","045970","040420","007370","041140","043610","036890","039010","009300","043200","042110","039740","039840","042420","039560","038460","039230","032820","001540","038530","039310","041190","036640","031330","030190","038620","039020","038950","036800","040610","038880","038680","041510","010280","037760","036480","038110","032500","039610","039240","038290","037440","038390","028150","036830","036810","036690","037370","036620","037350","038010","001810","036630","036710","037070","036560","016250","036030","035890","036930","032190","005290","036170","003100","036180","026040","037230","037460","037400","036490","033640","037330","036090","036200","024800","036260","027050","036120","035290","027040","027830","036000","035760","035810","035460","035620","035610","020710","012790","034940","033230","035080","005160","005990","034810","031390","033430","025770","033540","033500","030350","033310","033160","033320","009520","013810","033340","033200","033290","015710","033100","033050","033110","033130","032980","019210","026150","031310","032960","032680","032940","008290","032750","032860","032850","032790","032800","032620","032580","032540","028080","032280","012340","031510","030270","031860","031980","011560","024740","030960","030530","030520","021880","021040","029480","028040","028300","027710","023600","018310","003800","014190","012700","018000","025980","026910","017250","015750","020180","006730","025950","025900","025870","025880","002680","025550","025440","025320","024940","024950","014100","024840","024910","004780","013120","024830","024810","024880","024120","017000","024060","023910","001840","023900","023890","017650","010170","023790","023770","023760","005860","012860","023460","006050","023410","023440","006910","018290","023160","007530","001000","012620","011370","018700","014470","007720","006580","011320","018120","013720","009620","005670","007330","006140","019010","009780","008800","020400","014200","005710","016600","004590","016670","000440","014970","011040","008370","007390","002290","019540","007770","017890","003310","019660","017510","021080","008830","002230","009730","016920","013030","019550","019570","019590","006920"]

# 출력은 회사명, 주식,종가,고가,시가,저가 순으로 출력
for item in test:
    now_price = get_price(item)
    print(now_price)
conn.commit()
conn.close()