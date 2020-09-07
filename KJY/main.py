from bs4 import BeautifulSoup
import selenium.webdriver as webdriver
import urllib.parse
from urllib.request import Request, urlopen
from time import sleep
import pandas as pd

import pandas_csv #검색 결과를 .csv파일로 만들기 위한 파이썬 파일

search = input("검색어를 입력하세요 : " )
searching = str(search)
search = urllib.parse.quote(search)
url = 'https://www.instagram.com/explore/tags/'+str(search)+'/'
driver = webdriver.Chrome('chromedriver.exe')

driver.get(url) #검색어입력한 인스타그램 url 저장
sleep(3) #로딩 시간을 위한 속도조절 

SCROLL_PAUSE_TIME = 1.2  #인스타게시물 스크롤 속도 조절 ( 1.0 ~ 2.0까지 사양에 맞게 조절 )
reallink = []

while True: # 반복문 시작
    pageString = driver.page_source
    bs = BeautifulSoup(pageString, "lxml")

# 게시물 정보 
    for link1 in bs.find_all(name="div",attrs={"class":"Nnq7C weEfm"}):
        title = link1.select('a')[0] 
        real = title.attrs['href']
        reallink.append(real) 
        title = link1.select('a')[1] 
        real = title.attrs['href']
        reallink.append(real) 

# 페이지 스크롤
    last_height = driver.execute_script("return document.body.scrollHeight")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    #sleep(SCROLL_PAUSE_TIME)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(SCROLL_PAUSE_TIME)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
            
        else:
            last_height = new_height
            continue


hashtags2 = []

reallinknum = len(reallink)
print("총"+str(reallinknum)+"개의 데이터.")
try:  # 반복문 시작 ( print 명령어로 원하는 문자열인지 하나씩 확인해보시길 바랍니다.
    for i in range(0,reallinknum):
        hashtags2.append([])
        req = 'https://www.instagram.com/p'+reallink[i]
        driver.get(req)
        webpage = driver.page_source
        soup = BeautifulSoup(webpage, "html.parser")
        #print(soup)
        soup1 = str(soup.find_all(attrs={'class': 'e1e1d'}))
        #print(soup1)
        user_id = soup1.split('href="/')[1].split('/">')[0]
        #print(user_id)
        soup1 = str(soup.find_all(attrs={'class': 'Nm9Fw'}))
        #print(soup1)
        subValue = 'span'
        if(soup1=="[]"): #좋아요가 0개, 1개, n개 일경우 모두 소스가 다르다. 
            likes = '0'
        elif( soup1.find(subValue)==-1):
            likes = soup1.split('좋아요 ')[1].split('개')[0]
        elif( soup1.find(subValue)!=-1):
            likes = soup1.split('<span>')[1].split('</span>')[0]
        
        soup1 = str(soup.find_all(attrs={'class': 'xil3i'}))
        if(soup1=="[]"): #해쉬태그가 없을 경우 소스가 다르다.
            hashtags = '해쉬태그없음'
            insert_data = { "search" : searching,
                            "user_id" : user_id,
                            "좋아요" : likes,
                            "hashtags" : hashtags}
            pandas_csv.to_csv(insert_data)
        else:
            soup2 = soup1.split(',')
            soup2num = len(soup2)
            for j in range(0,soup2num):
                hashtags = soup2[j].split('#')[1].split('</a>')[0]
                print(hashtags) 
                insert_data = { "search" : searching,
                                "user_id" : user_id,
                                "좋아요" : likes,
                                "hashtags" : hashtags}
                #insert_data에 저장한 변수들 저장
                pandas_csv.to_csv(insert_data)

except:
    print("오류발생"+str(i+1)+"개의 데이터를 저장합니다.")   
    
    pandas_csv.to_csv(insert_data)  #insert_data에 저장한 데이터를 pandas_csv.py로 보냅니다.
print("저장성공")   
