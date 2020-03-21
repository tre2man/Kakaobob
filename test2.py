import openpyxl as xl

def strings():
    return "함수"

f = xl.Workbook()
file = f.active

a = 1
b = 5

file.cell(a,b,strings())
f.save("data.xlsx")

