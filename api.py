city = "37050"
key = "kb6LBBw2Jq1cFghDqy8h226dMGNgKfToicbxAfJI6KHpPZXpTqA76sygUnxxqnuUx984VWbCQbqQ05lXS0apPw%3D%3D"
bustop = "GMB132" #금오공대 종점
urlBustop = "http://openapi.tago.go.kr/openapi/service/ArvlInfoInqireService/getSttnAcctoArvlPrearngeInfoList?serviceKey="+ key +"&cityCode=" + city + "&nodeId=" + bustop
#금오공대종점 버스정류장 버스정보 url
urlBusEnd = "http://openapi.tago.go.kr/openapi/service/BusRouteInfoInqireService/getRouteNoList?serviceKey="+ key +"&cityCode=" + city + "&routeNo="
#버스정보 수집 urlBusEnd+버스번호