import bs4
import urllib.request

Restaurant=['학생식당','교직원 식당','푸름관','오름1동','오름3동']
Time=['조식','중식','석식']
Days=['월요일','화요일','수요일','목요일','금요일'',토요일','일요일']

urlStudent="http://www.kumoh.ac.kr/ko/restaurant01.do"
urlProfess="http://www.kumoh.ac.kr/ko/restaurant02.do"
urlPorum="http://dorm.kumoh.ac.kr/dorm/restaurant_menu01.do"
urlorum1="http://dorm.kumoh.ac.kr/dorm/restaurant_menu02.do"
urlorum2="http://dorm.kumoh.ac.kr/dorm/restaurant_menu03.do"

'''
월요일~일요일 중식 : 0~6
월요일~일요일 석식 : 7~13

@@@ 예외적으로 오름 1동은 중식->석식 @@@
'''

def returnMenu(url,num):
    html = bs4.BeautifulSoup(urllib.request.urlopen(url), "html.parser")
    menu = html.findAll("ul", {"class": "s-dot"})
    return menu[num].text

print(returnMenu(urlProfess,0))
