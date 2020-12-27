import time
import bs4
import urllib.request
import schedule
import openpyxl as xl

urlStudent = "http://www.kumoh.ac.kr/ko/restaurant01.do"
urlProfess = "http://www.kumoh.ac.kr/ko/restaurant02.do"
urlPorum = "http://dorm.kumoh.ac.kr/dorm/restaurant_menu01.do"
urlorum1 = "http://dorm.kumoh.ac.kr/dorm/restaurant_menu02.do"
urlorum3 = "http://dorm.kumoh.ac.kr/dorm/restaurant_menu03.do"

urlArr=[urlStudent,urlPorum,urlorum1,urlorum3,urlProfess]

for url in urlArr:
    html = bs4.BeautifulSoup(urllib.request.urlopen(url), "html.parser")
    print(html)
