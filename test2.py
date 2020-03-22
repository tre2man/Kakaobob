import openpyxl as xl
from flask import Flask,request,jsonify
import time
import bs4
import urllib.request

url = "https://www.weather.go.kr/w/weather/today.do#last-recent"

weatherbefore = "https://www.weather.go.kr/weather/climate/past_cal.jsp?stn=279&yy=2020&mm=3&obs=1&x=26&y=14"

html = bs4.BeautifulSoup(urllib.request.urlopen(url), "html.parser")
print(html)

