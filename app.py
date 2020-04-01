#앱 동작 부분

from flask import Flask,request,jsonify
import time
import module as md

import os
import sys

app = Flask(__name__)

ChoiceWeek=0
ChoiceRes=0
Lastindex = 1
user_max_number = 501    #저장 가능한 유저의 수


StudentTime=str("조식시간 : 08:30 ~ 09:30\n중식시간 : 11:30 ~ 14:00\n석식시간 : 17:30 ~ 18:30\n토 : 10:00~14:00\n일,공휴일 : 휴무")

ProfessTime=str("중식시간 : 11:30 ~ 14:00\n석식시간 : 17:30 ~ 18:30")

DomitoryTime=str("학기중\n\n조식 시간\n- 평일 : 07:30 ~ 09:30\n- 주말 : 08:00 ~ 09:30\n중식 시간\n- 평일 : 11:30 ~ 13:30"
                 "\n- 주말 : 12:00 ~ 13:30\n석식 시간\n- 평일 : 17:00 ~ 19:00\n- 주말 : 17:00 ~ 18:30\n\n방학중\n\n"
                 "조식 시간- 08:00 ~ 09:30\n중식 시간- 12:00 ~ 13:30\n석식 시간- 17:00 ~ 18:30")


@app.route('/message', methods=['POST'])  #json으로 들어온 사용자 요청을 보고 판단
def bob():

    contents = request.get_json()    #사용자가 보낸 메세지 입력

    says = contents['userRequest']['utterance']         #사용자의 발화 추출
    user_key = contents['userRequest']['user']['id']    #사용자의 id 추출

    if says==u"학생식당":
        response_data = md.returnjsonChoiceday()
        md.saveDBres(user_key, 0)

    elif says==u"푸름관":
        response_data = md.returnjsonChoiceday()
        md.saveDBres(user_key, 1)

    elif says==u"오름1동":
        response_data = md.returnjsonChoiceday()
        md.saveDBres(user_key, 2)

    elif says == u"오름3동":
        response_data = md.returnjsonChoiceday()
        md.saveDBres(user_key, 3)

    elif says==u"교직원":
        response_data = md.returnjsonChoiceday()
        md.saveDBres(user_key, 4)

    elif says==u"분식당":
        response_data = md.returnjsonChoiceday()
        md.saveDBres(user_key, 5)

    elif says==u"오늘":
        ChoiceWeek = time.localtime().tm_wday
        response_data = md.returnMenujson(md.findRes(user_key),ChoiceWeek)

    elif says==u"월요일":
        ChoiceWeek = 0
        response_data = md.returnMenujson(md.findRes(user_key),ChoiceWeek)

    elif says==u"화요일":
        ChoiceWeek = 1
        response_data = md.returnMenujson(md.findRes(user_key),ChoiceWeek)

    elif says==u"수요일":
        ChoiceWeek = 2
        response_data = md.returnMenujson(md.findRes(user_key),ChoiceWeek)

    elif says==u"목요일":
        ChoiceWeek = 3
        response_data = md.returnMenujson(md.findRes(user_key),ChoiceWeek)

    elif says==u"금요일":
        ChoiceWeek = 4
        response_data = md.returnMenujson(md.findRes(user_key),ChoiceWeek)

    elif says==u"토요일":
        ChoiceWeek = 5
        response_data = md.returnMenujson(md.findRes(user_key),ChoiceWeek)

    elif says==u"일요일":
        ChoiceWeek = 6
        response_data = md.returnMenujson(md.findRes(user_key),ChoiceWeek)

    elif says==u"처음으로" :
        response_data = md.jsonMainmenu

    elif says==u"식단 정보":
        response_data = md.jsonChoiceRes

    elif says==u"식당 이용 가능 시간":
        response_data = md.jsonChoiceAvailableTime

    elif says==u"학생식당 시간":
        response_data = md.returnAvaliableTime(StudentTime)

    elif says == u"기숙사 시간":
        response_data = md.returnAvaliableTime(DomitoryTime)

    elif says == u"교직원 시간":
        response_data = md.returnAvaliableTime(ProfessTime)

    elif says == u"날씨 정보":
        response_data = md.returnWeatherjson()

    elif says == u"버스 정보":
        response_data = md.returnBusTime()

    else :
        response_data = md.jsonMainmenu

    return jsonify(response_data)

if __name__=="__main__":
     app.run(host="0.0.0.0", port=5000)