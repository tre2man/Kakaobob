import time
import bs4
import urllib.request
import schedule
import openpyxl as xl


Restaurant=["학생식당","푸름관","오름1동","오름3동","교직원 식당"]

ChoiceUrl=""
ChoiceDay=0
ChoiceRes=0

urlStudent="http://www.kumoh.ac.kr/ko/restaurant01.do"
urlProfess="http://www.kumoh.ac.kr/ko/restaurant02.do"
urlPorum="http://dorm.kumoh.ac.kr/dorm/restaurant_menu01.do"
urlorum1="http://dorm.kumoh.ac.kr/dorm/restaurant_menu02.do"
urlorum3="http://dorm.kumoh.ac.kr/dorm/restaurant_menu03.do"
urlBunsic="http://www.kumoh.ac.kr/ko/restaurant04.do"

urlArr=[urlStudent,urlPorum,urlorum1,urlorum3,urlProfess,urlBunsic]
saveMenu = []  # 6개의 식당, 7개의 요일


###변수 선언 완료
###함수 선언 시작


def returnMenu(url,num):  #식단 문자열을 반환하는 함수 (식당종류,날짜)

    global ChoiceRes

    html = bs4.BeautifulSoup(urllib.request.urlopen(url), "html.parser")
    menus=html.find("td")
    menu=str(menus.text)  #bs4 자료형을 String 형태로 변환, 식단의 존재 유무 판별

    if menu=="등록된 메뉴가 없습니다." : #식단이 없을경우(기숙사 식당 주로)
        return "등록된 메뉴가 없습니다. 😥"

    else:                              #식단이 있을경우
        menu = html.findAll("ul", {"class": "s-dot"})
        menuEnd = str(menu[num].text.rstrip("\n"))
        menuEnd = menuEnd.lstrip()

        days=html.findAll("th",{"scope":{"col"}})
        day=str(days[num].text.lstrip())

        if menuEnd != "" :
            if ChoiceRes==2:        #오름1동, 중식->조식
                menuEnd2 = str(menu[num + 7].text.rstrip("\n"))
                menuEnd2 = menuEnd2.lstrip()
                return f"선택한 날짜 : {day}\n아침메뉴\n\n{menuEnd}\n\n저녁메뉴\n\n{menuEnd2}"

            elif ChoiceRes==5:      #분식당, 1일 1메뉴
                return f"선택한 날짜 : {day}\n{menuEnd}"

            else:                    #점심과 저녁
                menuEnd2 = str(menu[num + 7].text.rstrip("\n"))
                menuEnd2 = menuEnd2.lstrip()
                return f"선택한 날짜 : {day}\n점심메뉴\n\n{menuEnd}\n\n저녁메뉴\n\n{menuEnd2}"

        else:
            return "등록된 메뉴가 없습니다. 😥"


def saveMenuArr():  #금오공대 전체 메뉴를 저장하기 위한 함수

    day = str(time.localtime().tm_mday)
    min = str(time.localtime().tm_min)
    sec = str(time.localtime().tm_sec)
    print(f"Save Start at {day} day, {min} min {sec} sec")

    f = xl.Workbook()
    file = f.active

    global ChoiceRes
    global saveMenu
    a = -1
    ChoiceRes = 0

    for i in urlArr:   #식당 루프
        b = 0
        a += 1
        for j in range (7) :  #번호 루프
            file.cell(a+1,b+1,returnMenu(i,j))  #해당하는 셀에 메뉴 정보를 저장
            b += 1
        ChoiceRes += 1

    f.save('files/data.xlsx')  #최종적으로 파일 저장

    min = str(time.localtime().tm_min)
    sec = str(time.localtime().tm_sec)
    print(f"Save Finish at {day} day, {min} min {sec} sec")


def openMenu(a,b):  #해당 값의 셀 내용 반환하는 함수(x,y)

    f = xl.load_workbook('files/data.xlsx',data_only=True)
    file = f['Sheet']

    return file.cell(a+1,b+1).value


saveMenuArr()  #프로그램 최초 실행 시 메뉴 리프레시(저장)

schedule.every().monday.at("00:01").do(saveMenuArr)   #월요일 00:01 마다 크롤링

while True:
    schedule.run_pending()
    time.sleep(1)



