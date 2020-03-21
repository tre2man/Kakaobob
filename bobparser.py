###TEST CODE###

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

        days=html.findAll("th",{"scope":{"col"}})
        day=str(days[num].text.lstrip())

        if menuEnd != "" :
            if ChoiceRes==2: #오름1동, 중식->조식
                menuEnd2 = str(menu[num + 7].text.rstrip("\n"))
                return "선택한 날짜 : "+day+"\n"+"아침메뉴\n\n"+menuEnd.lstrip()+"\n\n저녁메뉴\n\n"+menuEnd2.lstrip()

            elif ChoiceRes==5: #분식당, 1일 1메뉴
                return "선택한 날짜 : "+day+"\n"+menuEnd.lstrip()

            else:  #점심과 저녁
                menuEnd2 = str(menu[num + 7].text.rstrip("\n"))
                return "선택한 날짜 : "+day+"\n"+"점심메뉴\n\n"+menuEnd.lstrip()+"\n\n저녁메뉴\n\n"+menuEnd2.lstrip()

        else:
            return "등록된 메뉴가 없습니다. 😥"


def saveMenuArr():

    print("Save Start!!")

    f = xl.Workbook()
    file = f.active

    a = -1
    global ChoiceRes
    global saveMenu
    ChoiceRes = 0

    for i in urlArr:   #식당 루프
        b = 0
        a += 1
        for j in range (7) :  #번호 루프
            file.cell(a+1,b+1,returnMenu(i,j))
            b += 1
        ChoiceRes += 1

    f.save('files/data.xlsx')
    print("Save Finish!!")


def openMenu(a,b):

    f = xl.load_workbook('files/data.xlsx',data_only=True)
    file = f['Sheet']

    return file.cell(a+1,b+1).value


saveMenuArr()


schedule.every().day.at("10:30").do(saveMenuArr)
schedule.every().day.at("10:30").do(saveMenuArr)

while True:
    schedule.run_pending()
    time.sleep(1)



