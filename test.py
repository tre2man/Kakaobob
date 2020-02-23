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

urlBus = "http://bis.gumi.go.kr/map/BusMap.do"

'''
월요일~일요일 중식 : 0~6
월요일~일요일 석식 : 7~13
@@@ 예외적으로 오름 1동은 중식->석식 @@@
'''



def returnMenu(url,num):  #식단을 보여줄수 있게 하는 함수 (링크,식단종류)
    html = bs4.BeautifulSoup(urllib.request.urlopen(url), "html.parser")
    menus=html.find("td")
    menu=str(menus.text)  #bs4 자료형을 String 형태로 변환, 식단의 존재 유무 판별

    if(menu=="등록된 메뉴가 없습니다."): #식단이 없을경우
        return menu
    else:                              #식단이 있을경우
        html = bs4.BeautifulSoup(urllib.request.urlopen(url), "html.parser")
        menu = html.findAll("ul", {"class": "s-dot"})
        return menu[num].text


def returnAvaliableTimeDormitory(url):  #기숙사 식당 이용 시간을 리턴하는 함수
    html = bs4.BeautifulSoup(urllib.request.urlopen("https://search.naver.com/search.naver?where=nexearch&sm=tab_etc&mra=blQ3&query=%EB%8C%80%EC%A0%84%20%EB%AF%B8%EC%84%B8%EB%A8%BC%EC%A7%80"), "html.parser")
    Times=html.findAll("span",{"class":"value"})
    #Time=Times.find("em",{"",""})
    return Times[0].text


def returnAvaliableTime(url):  #전체식당 이용 시간을 리턴하는 함수
    html = bs4.BeautifulSoup(urllib.request.urlopen(url), "html.parser")
    Time=html.findAll("ul",{"class":"ul-h-list01"})
    return Time[1].text


Timess=returnAvaliableTimeDormitory(urlPorum)

print(Timess)