import openpyxl as xl
from flask import Flask,request,jsonify
import time
import bs4
import urllib.request
import schedule

url = "https://www.weather.go.kr/w/weather/today.do#last-recent"

weatherbefore = "https://www.weather.go.kr/weather/climate/past_cal.jsp?stn=279&yy=2020&mm=3&obs=1&x=26&y=14"

html = bs4.BeautifulSoup(urllib.request.urlopen(url), "html.parser")

def job():
    day = str(time.localtime().tm_mday)
    min = str(time.localtime().tm_min)
    sec = str(time.localtime().tm_sec)
    print(f"Save Start at {day} day, {min} min {sec} sec")

schedule.every(1).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)




