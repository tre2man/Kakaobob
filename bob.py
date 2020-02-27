from flask import Flask,request,jsonify
import time
import bs4
import urllib.request

import os
import sys

app = Flask(__name__)

#식당성정->날짜설정->아침점심저녁 설정->처음으로

Restaurant=["학생식당","푸름관","오름1동","오름3동","교직원 식당"]
week=["월요일","화요일","수요일","목요일","금요일","토요일","일요일"]

ChoiceUrl=""
ChoiceDay=0
ChoiceRes=0

urlStudent="http://www.kumoh.ac.kr/ko/restaurant01.do"
urlProfess="http://www.kumoh.ac.kr/ko/restaurant02.do"
urlPorum="http://dorm.kumoh.ac.kr/dorm/restaurant_menu01.do"
urlorum1="http://dorm.kumoh.ac.kr/dorm/restaurant_menu02.do"
urlorum3="http://dorm.kumoh.ac.kr/dorm/restaurant_menu03.do"
urlBunsic="http://www.kumoh.ac.kr/ko/restaurant04.do"

'''
월요일~일요일 중식 : 0~6
월요일~일요일 석식 : 7~13

@@@ 예외적으로 오름 1동은 중식->조식 @@@
'''

jsonChoiceDay = {
    "version": "2.0",
    "template": {"outputs": [{"simpleText": {"text": "요일을 선택해 주세요.\n\n오늘은"+str(time.localtime().tm_year)+"년"+str(time.localtime().tm_mon)+"월"+str(time.localtime().tm_mday)+"일"+week[time.localtime().tm_wday]+"입니다."}}],
                 "quickReplies": [{"label": "오늘", "action": "message", "messageText": "오늘"},
                                  {"label": "월요일", "action": "message", "messageText": "월요일"},
                                  {"label": "화요일", "action": "message", "messageText": "화요일"},
                                  {"label": "수요일", "action": "message", "messageText": "수요일"},
                                  {"label": "목요일", "action": "message", "messageText": "목요일"},
                                  {"label": "금요일", "action": "message", "messageText": "금요일"},
                                  {"label": "토요일", "action": "message", "messageText": "토요일"},
                                  {"label": "일요일", "action": "message", "messageText": "일요일"}
                                  ]
                 }
}

jsonChoiceRes = {
    "version": "2.0",
    "template": {"outputs": [{"simpleText": {"text": "식당을 선택해 주세요."}}],
                 "quickReplies": [{"label": "학생식당", "action": "message", "messageText": "학생식당"},
                                  {"label": "푸름관", "action": "message", "messageText": "푸름관"},
                                  {"label": "오름1동", "action": "message", "messageText": "오름1동"},
                                  {"label": "오름3동", "action": "message", "messageText": "오름3동"},
                                  {"label": "교직원", "action": "message", "messageText": "교직원"},
                                  ]
                 }
}

jsonChoiceAvailableTime = {
    "version": "2.0",
    "template": {"outputs": [{"simpleText": {"text": "식당을 선택해 주세요."}}],
                 "quickReplies": [{"label": "학생식당", "action": "message", "messageText": "학생식당 시간"},
                                  {"label": "기숙사", "action": "message", "messageText": "기숙사 시간"},
                                  {"label": "교직원", "action": "message", "messageText": "교직원 시간"},
                                  ]
                 }
}

StudentTime="조식시간 : 08:30 ~ 09:30\n중식시간 : 11:30 ~ 14:00\n석식시간 : 17:30 ~ 18:30\n토 : 10:00~14:00\n일,공휴일 : 휴무"
ProfessTime="중식시간 : 11:30 ~ 14:00\n석식시간 : 17:30 ~ 18:30"
DomitoryTime="학기중\n\n조식 시간\n- 평일 : 07:30 ~ 09:30\n- 주말 : 08:00 ~ 09:30\n중식 시간\n- 평일 : 11:30 ~ 13:30\n- 주말 : 12:00 ~ 13:30\n석식 시간\n- 평일 : 17:00 ~ 19:00\n- 주말 : 17:00 ~ 18:30\n\n방학중\n\n조식 시간- 08:00 ~ 09:30\n중식 시간- 12:00 ~ 13:30\n석식 시간- 17:00 ~ 18:30"


def returnMenu(url,num):  #식단을 보여줄수 있게 하는 함수 (링크,식단종류)

    global ChoiceRes

    html = bs4.BeautifulSoup(urllib.request.urlopen(url), "html.parser")
    menus=html.find("td")
    menu=str(menus.text)  #bs4 자료형을 String 형태로 변환, 식단의 존재 유무 판별

    if(menu=="등록된 메뉴가 없습니다."): #식단이 없을경우(기숙사 식당 주로)
        return menu

    else:                              #식단이 있을경우
        html = bs4.BeautifulSoup(urllib.request.urlopen(url), "html.parser")
        menu = html.findAll("ul", {"class": "s-dot"})
        menuEnd = str(menu[num].text.rstrip("\n"))

        if menuEnd != "" :
            if ChoiceRes==1: #중식->조식
                menuEnd2 = str(menu[num + 7].text.rstrip("\n"))
                return "아침메뉴\n\n"+menuEnd.lstrip()+"\n\n저녁메뉴\n\n"+menuEnd2.lstrip()

            elif ChoiceRes==5: #분식당, 1일 1메뉴
                return menuEnd.lstrip()

            else:  #점심과 저녁
                menuEnd2 = str(menu[num + 7].text.rstrip("\n"))
                return "점심메뉴\n\n"+menuEnd.lstrip()+"\n\n저녁메뉴\n\n"+menuEnd2.lstrip()

        else:
            return "등록된 메뉴가 없습니다."

def returnAvaliableTime(index):  #식당 이용 가능 시간을 리턴하는 함수
    temp={
         "version": "2.0",
         "template": {
             "outputs": [{"simpleText": {"text": index}}],
             "quickReplies": [{"label": "처음으로", "action": "message", "messageText": "처음으로"},
                              ]
                     }
         }

    return temp


def returnMenujson(url,num):
    temp={
        "version": "2.0",
        "template": {"outputs": [{"simpleText": {"text": returnMenu(url,num)}}],
                     "quickReplies": [{"label": "처음으로", "action": "message", "messageText": "처음으로"},
                                      ]
                     }
        }

    return temp

@app.route('/message', methods=['POST'])  #json으로 들어온 사용자 요청을 보고 판단
def bob():

    content = request.get_json() #사용자가 보낸 메세지 입력
    content = content['userRequest']
    content = content['utterance']

    global ChoiceUrl
    global ChoiceDay
    global ChoiceRes
    global jsonChoiceDay
    global jsonChoiceRes

    if content==u"학생식당":
        response_data=jsonChoiceDay
        ChoiceUrl=urlStudent
        ChoiceRes=0

    elif content==u"푸름관":
        response_data=jsonChoiceDay
        ChoiceUrl=urlPorum
        ChoiceRes = 1

    elif content==u"오름1동":
        response_data=jsonChoiceDay
        ChoiceUrl=urlorum1
        ChoiceRes = 2

    elif content == u"오름3동":
        response_data=jsonChoiceDay
        ChoiceUrl=urlorum3
        ChoiceRes = 3

    elif content==u"교직원":
        response_data=jsonChoiceDay
        ChoiceUrl=urlProfess
        ChoiceRes = 4

    elif content==u"분식당":
        response_data=jsonChoiceDay
        ChoiceUrl=urlBunsic
        ChoiceRes = 5

    elif content==u"오늘":
        ChoiceDay = time.localtime().tm_wday
        response_data = returnMenujson(ChoiceUrl,ChoiceDay)

    elif content==u"월":
        ChoiceDay = 0
        response_data = returnMenujson(ChoiceUrl,ChoiceDay)

    elif content==u"화":
        ChoiceDay = 1
        response_data = returnMenujson(ChoiceUrl,ChoiceDay)

    elif content==u"수":
        ChoiceDay = 2
        response_data = returnMenujson(ChoiceUrl,ChoiceDay)

    elif content==u"목":
        ChoiceDay = 3
        response_data = returnMenujson(ChoiceUrl,ChoiceDay)

    elif content==u"금":
        ChoiceDay = 4
        response_data = returnMenujson(ChoiceUrl,ChoiceDay)

    elif content==u"토":
        ChoiceDay = 5
        response_data = returnMenujson(ChoiceUrl,ChoiceDay)

    elif content==u"일":
        ChoiceDay = 6
        response_data = returnMenujson(ChoiceUrl,ChoiceDay)

    elif content==u"처음으로":
        response_data=jsonChoiceRes

    elif content==u"식당 이용 가능 시간":
        response_data=jsonChoiceAvailableTime

    elif content==u"학생식당 시간":
        response_data=returnAvaliableTime(StudentTime)

    elif content == u"기숙사 시간":
        response_data = returnAvaliableTime(DomitoryTime)

    elif content == u"교직원 시간":
        response_data = returnAvaliableTime(ProfessTime)

    else :
        response_data = jsonChoiceRes

    return jsonify(response_data)

if __name__=="__main__":
     app.run(host="0.0.0.0", port=5000)


