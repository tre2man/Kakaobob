from flask import Flask, request, jsonify
import bs4
import urllib.request
import os
import sys
import time

app = Flask(__name__)

Restaurant = ['학생식당', '교직원 식당', '푸름관', '오름1동', '오름3동']
Time = ['조식', '중식', '석식']
Days = ['오늘', '월요일', '화요일', '수요일', '목요일', '금요일'',토요일', '일요일']
Reset = '처음으로'

# 식당성정->날짜설정->아침점심저녁 설정->처음으로

ChoiceUrl = ""
ChoiceDay = 0
ChoiceRes = 0

urlStudent = "http://www.kumoh.ac.kr/ko/restaurant01.do"
urlProfess = "http://www.kumoh.ac.kr/ko/restaurant02.do"
urlPorum = "http://dorm.kumoh.ac.kr/dorm/restaurant_menu01.do"
urlorum1 = "http://dorm.kumoh.ac.kr/dorm/restaurant_menu02.do"
urlorum3 = "http://dorm.kumoh.ac.kr/dorm/restaurant_menu03.do"

'''
월요일~일요일 중식 : 0~6
월요일~일요일 석식 : 7~13
@@@ 예외적으로 오름 1동은 중식->석식 @@@
'''


def returnMenu(url, num):  # 식단을 보여줄수 있게 하는 함수 (링크,식단종류)
    html = bs4.BeautifulSoup(urllib.request.urlopen(url), "html.parser")
    menu = html.findAll("ul", {"class": "s-dot"})
    return menu[num].text


@app.route('/keyboard')  # 최초로 채팅방에 접속시 보여 줄 버튼
def keyboard():
    return jsonify({
        "version": "2.0",
        "template": {"outputs": [{"carousel": {"type": "basicCard", "items": [{"title": "", "description": "안녕하세"}]}}]}
    })


@app.route('/message', methods=['POST'])  # json으로 들어온 사용자 요청을 보고 판단,테스트로 저녁메뉴만 봅시다
def bob():
    content = request.get_json()  # 사용자가 보낸 메세지 입력
    content = content['userRequest']
    content = content['utterance']

    global ChoiceUrl
    global ChoiceDay
    global ChoiceRes

    today = time.localtime().tm_wday + 7  # 저녁일 경우에는 +7

    if content == u"선택":
        response_data = {
            "version": "2.0",
            "template": {"outputs": [{"carousel": {"type": "basicCard", "items": [
                {"title": "", "description": returnMenu(urlPorum, today)}]}}]}
        }

    elif content == u"푸름관":
        response_data = {
            "version": "2.0",
            "template": {"outputs": [{"carousel": {"type": "basicCard", "items": [
                {"title": "", "description": returnMenu(urlPorum, today)}]}}]}
        }

    elif content == u"교직원":
        response_data = {
            "version": "2.0",
            "template": {"outputs": [{"carousel": {"type": "basicCard", "items": [
                {"title": "", "description": returnMenu(urlProfess, today)}]}}]}
        }

    elif content == u"오름1동":
        response_data = {
            "version": "2.0",
            "template": {"outputs": [{"carousel": {"type": "basicCard", "items": [
                {"title": "", "description": returnMenu(urlorum1, today)}]}}]}
        }

    elif content == u"오름3동":
        response_data = {
            "version": "2.0",
            "template": {"outputs": [{"carousel": {"type": "basicCard", "items": [
                {"title": "", "description": returnMenu(urlorum3, today)}]}}]}
        }

    elif content == u"학생식당":
        response_data = {
            "version": "2.0",
            "template": {"outputs": [{"carousel": {"type": "basicCard", "items": [
                {"title": "", "description": returnMenu(urlStudent, today)}]}}]}
        }


    elif content == u"안녕":
        response_data = {
            "version": "2.0",
            "template": {
                "outputs": [{"carousel": {"type": "basicCard", "items": [{"title": "", "description": "안녕"}]}}]}
        }

    '''
    if user_input == Reset:  # 맨 마지막에서 다시 처음으로 올 때
        response_data = {'message': {"text": "식당을 선택해 주세요"}, "keyboard": {"buttons": Restaurant, "type": "buttons", }}
    elif user_input==Restaurant[0]:   #학생식당 선택할 경우
        response_data={'message':{"text":"날짜를 선택해 주세요"},"keyboard" : {"buttons" : Days,"type" : "buttons",}}
        ChoiceUrl=urlStudent
        ChoiceRes = 0
    elif user_input==Restaurant[1]:   #교직원식당 선택할 경우
        response_data={'message':{"text":"날짜를 선택해 주세요"},"keyboard" : {"buttons" : Days,"type" : "buttons",}}
        ChoiceUrl=urlProfess
        ChoiceRes = 1
    elif user_input==Restaurant[2]:   #푸름1 선택할 경우
        response_data={'message':{"text":"날짜를 선택해 주세요"},"keyboard" : {"buttons" : Days,"type" : "buttons",}}
        ChoiceUrl=urlPorum
        ChoiceRes = 2
    elif user_input==Restaurant[3]:   #오름1 선택할 경우
        response_data={'message':{"text":"날짜를 선택해 주세요"},"keyboard" : {"buttons" : Days,"type" : "buttons",}}
        ChoiceUrl=urlorum1
        ChoiceRes = 3
    elif user_input==Restaurant[4]:   #오름3 선택할 경우
        response_data={'message':{"text":"날짜를 선택해 주세요"},"keyboard" : {"buttons" : Days,"type" : "buttons",}}
        ChoiceUrl=urlorum3
        ChoiceRes = 4
    elif user_input==Days[0]:   #오늘 선택한 경우
        response_data={'message':{"text":"시간을 선택해 주세요"},"keyboard" : {"buttons" : Time,"type" : "buttons",}}
        ChoiceDay=time.localtime().tm_wday
    elif user_input==Days[1]:   #월요일 선택한 경우
        response_data={'message':{"text":"시간을 선택해 주세요"},"keyboard" : {"buttons" : Time,"type" : "buttons",}}
        ChoiceDay=0
    elif user_input==Days[2]:   #화요일 선택한 경우
        response_data={'message':{"text":"시간을 선택해 주세요"},"keyboard" : {"buttons" : Time,"type" : "buttons",}}
        ChoiceDay=1
    elif user_input==Days[3]:   #수요일 선택한 경우
        response_data={'message':{"text":"시간을 선택해 주세요"},"keyboard" : {"buttons" : Time,"type" : "buttons",}}
        ChoiceDay=2
    elif user_input==Days[4]:   #목요일 선택한 경우
        response_data={'message':{"text":"시간을 선택해 주세요"},"keyboard" : {"buttons" : Time,"type" : "buttons",}}
        ChoiceDay=3
    elif user_input==Days[5]:   #금요일 선택한 경우
        response_data={'message':{"text":"시간을 선택해 주세요"},"keyboard" : {"buttons" : Time,"type" : "buttons",}}
        ChoiceDay=4
    elif user_input==Days[6]:   #토요일 선택한 경우
        response_data={'message':{"text":"시간을 선택해 주세요"},"keyboard" : {"buttons" : Time,"type" : "buttons",}}
        ChoiceDay=5
    elif user_input==Days[7]:   #일요일 선택한 경우
        response_data={'message':{"text":"시간을 선택해 주세요"},"keyboard" : {"buttons" : Time,"type" : "buttons",}}
        ChoiceDay=6
    elif user_input==Time[0]:   #조식 선택한 경우
        if ChoiceUrl!=urlorum1 :  #오름 1동 외에 나머지를 선택
            response_data={'message':{"text": Restaurant[ChoiceRes]+"은 조식이 없습니다. 다시 선택해 주세요."},"keyboard" : {"buttons" : Time,"type" : "buttons",}}
        else:                     #오름 1동&&조식
            response_data={'message': {"text": returnMenu(ChoiceUrl,ChoiceDay)}, "keyboard": {"buttons": Reset, "type": "buttons", }}
            ChoiceDay=0
            ChoiceUrl=""
    elif user_input==Time[1]:   #중식 선택한 경우
        response_data={'message': {"text": returnMenu(ChoiceUrl,ChoiceDay)}, "keyboard": {"buttons": Reset, "type": "buttons", }}
        ChoiceDay = 0
        ChoiceUrl = ""
    elif user_input==Time[2]:   #석식 선택한 경우
        ChoiceDay+=7
        response_data={'message': {"text": returnMenu(ChoiceUrl,ChoiceDay)}, "keyboard": {"buttons": Reset, "type": "buttons", }}

    '''

    return jsonify(response_data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)