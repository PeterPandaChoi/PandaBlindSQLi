# PandaBlindSQLi
<br/>'Panda Blind SQL injection' (or 'PandaBlindSQLi') is a rudimentary tool for automating 'Errorbased SQL injection' pentest Process, currently specialized in post method, Coded fully in Python, with a few lib.
<br/>'Panda Blind SQLi'는 Blind SQL injection의 침투테스트를 위한 초보적인 툴이며, 몇몇 라이브러리를 포함한 파이썬으로 코딩하였습니다.
<br/>해당 코드의 첫 커밋은 블로그에 상술되어 있습니다. [tba]

# Specification
<br/>method : POST
<br/>parameter(fixed at the moment) : UserId, Password, Submit
<br/>Utilized BinSearch Func : ascii(), substr()
<br/>attack format : normaltic' and (ascii(substr((),1,1)) > 0) and '1'='1


# Required library 필요한 라이브러리
1. requests                **[required for sending requests to web]**
2. parse                   [unnecessary at the moment]
3. diff_match_patch        **[used for checking differences between two requests]**
4. bs4 (or BeautifulSoap)  **[used for stripping html tags and etcs]**
5. lxml                    [you need this to use bs4]

~~~
pip install requests
pip install parse
pip install diff_match_patch
pip install bs4
pip install lxml
~~~

# Basic Process
This Union SQL Injection goes through 7 steps.
(0. Function Def.)
1. Find SQLi point [ input : Links and Param(NOT YET) ]
2. select Phrase Test 
3. Attack Format 
4. DB Name, by using "Database()" payload.
5. Table Names, by checking schema [ choose a table to inspect further ]
6. Column Names, by checking schema [ choose a column to inspect further ]
7. Row Names 


# Future Plan
1. Get/POST method selection
2. parameter Customize
3. Scanning every column of a table
4. Scanning row of every column.
5. or even multiple table

# Ref.
Rudimentary Algorithm record & explanation(KR) : tba
