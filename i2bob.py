from flask import Flask,request,jsonify
import bs4
import urllib.request
import os
import time

app = Flask(__name__)

Restaurant=['학생식당','교직원 식당','푸름관','오름1동','오름3동']
Time=['조식','중식','석식']
Days=['오늘','월요일','화요일','수요일','목요일','금요일'',토요일','일요일']
Reset='처음으로'

#식당성정->날짜설정->아침점심저녁 설정->처음으로

ChoiceUrl=""
ChoiceDay=0
ChoiceRes=0

urlStudent="http://www.kumoh.ac.kr/ko/restaurant01.do"
urlProfess="http://www.kumoh.ac.kr/ko/restaurant02.do"
urlPorum="http://dorm.kumoh.ac.kr/dorm/restaurant_menu01.do"
urlorum1="http://dorm.kumoh.ac.kr/dorm/restaurant_menu02.do"
urlorum3="http://dorm.kumoh.ac.kr/dorm/restaurant_menu03.do"

'''
월요일~일요일 중식 : 0~6
월요일~일요일 석식 : 7~13

@@@ 예외적으로 오름 1동은 중식->석식 @@@
'''

def returnMenu(url,num):  #식단을 보여줄수 있게 하는 함수 (링크,식단종류)
    html = bs4.BeautifulSoup(urllib.request.urlopen(url), "html.parser")
    menu = html.findAll("ul", {"class": "s-dot"})
    return menu[num].text


@app.route('/keyboard')  #최초로 채팅방에 접속시 보여 줄 버튼
def keyboard():
    return jsonify({
        "type" : "buttons",
        "buttons" : Restaurant
       })

@app.route('/message',methods=["POST"])  #json으로 들어온 사용자 요청을 보고 판단
def bob():
    dataRecieve = request.get_json()   #사용자가 보낸 메시지 입력
    user_input=dataRecieve["content"]
    global ChoiceUrl
    global ChoiceDay
    global ChoiceRes

    response_data={"version":"2.0",
                   "template":{"outputs":[{"simpletext":{"text":"식당을 선택해 주세요."}}]},
                   "context":{},
                   "data":{}
                   }

    return jsonify(response_data)


if __name__=="__main__":
     app.run(host="0.0.0.0", port=5000)