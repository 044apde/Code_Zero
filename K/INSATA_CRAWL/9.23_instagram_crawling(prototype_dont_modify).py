from urllib.request import urlopen
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import selenium.webdriver.common.keys
from tqdm import tqdm
import pandas as pd
from requests import Request
from flask import Request
from urllib import request
import re
import datetime
import os
import zipfile
import shutil
import unicodedata

# 크롬이 모바일 장치로 인식되도록 속성을 변경한다.
# options = webdriver.ChromeOptions()
# mobile_emulation = {"deviceName": "Nexus 5"}
# options.add_experimental_option("mobileEmulation", mobile_emulation)

# 크롬 브라우저를 백그라운드 프로세스 형태로 실행시키고자 하는 경우 아래의 옵션도 추가한다.
#options.add_argument('headless')
#options.add_argument('window-size=1920x1080')
#options.add_argument("disable-gpu")



# 작업시간을 알리기 위한, 현재 시간 변수 지정
now = datetime.datetime.now()

# 드라이버 변수 지정, 패스 지정
driver = webdriver.Chrome(executable_path ="./ChromeDriver/chromedriver.exe")
driver.implicitly_wait(5)

# 검색할 url 지정
def insta_searching(word):
    url = 'https://www.instagram.com/explore/tags/' + word

    return url

# 함수 정의: 첫번째 게시물 찾아 클릭 함수 만들기
def select_first(driver):
    # 열린 크롬으로 개발자 도구를 활용하여 첫번째 게시물 태그 확인 (<div clas="_9AhH0"></div>)
    first = driver.find_element_by_css_selector('div._9AhH0')
    first.click()
    time.sleep(4)

# 함수 정의: 콘텐츠 불러오기
def get_content(driver):
    # 1. 현재 페이지의 HTML 정보 가져오기
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # 2. 본문 내용 가오기
    try:                            # 여러 태그중에서 첫번째([0]) 태그를 선택한다.
        content = soup.select('div.C4VMK > span')[0].text
        content = unicodedata.normalize('NFC', content)
                                    # 첫 게시글 본문 내용이 <div class = 'C4VMK'> 임을 알 수 있다.
                                    # 태그명이 div, class명이 C4VMK인 태그 아래에 있는 span 태그를 모두 선택한다.

    except:
        content = ''

    # 3. 본문 내용에서 해시태그 가져오기(정규표현식을 활용한다.)
                                    # conetent 변수의 본문 내용 중 #으로 시작하며,
                                    # #뒤에 연속된 문자(공백이나 #, \기호가 아닌 경우)를 모두 찾아 tags 변수에 저장한
    tags = str(re.findall(r'#[^\s#,\\]+',  content))
    tags = unicodedata.normalize('NFC', tags)

    # 4. 작성일자 가져오기
    try:
        date = soup.select('time._1o9PC.Nzb55')[0]['datetime'][:10] # 앞에서부터 10자리 글자
    except:
        date = ''

    # 5. 좋아요 수 가져오기
    try:
        like = soup.select('div.Nm9Fw > button')[0].text
        like = like[4:-1]
    except:
        like = 0

    # 6. 위치 정보 가져오기
    try:
        place = soup.select('div.JF9hh')[0].text
    except:
        place = ''


    # 7. 유저 아이디 가져오기
    try:
        ID = soup.select('div.e1e1d')[0].text
    except:
        ID = ''

    # 8. 이미지 URL 가져오기
    try:
        IMG = soup.select()
    except:



    # 8. 수집한 정보 저장하기
    data = [ID, content, date, like, place, tags]
    return data




# 함수 정의: 다음 페이지로 넘어가기.
def move_next(driver):
    right = driver.find_element_by_css_selector('a._65Bje.coreSpriteRightPaginationArrow')
    right.click()
    time.sleep(3)

#1. 크롬으로 인스타그램 - '술담화' 검색한다.
print("CODE-ZERO : Instagram_Crawling Started...")
time.sleep(2)
word = "술담화"
url = insta_searching(word)
driver.get(url)
print("Open Chrome by webdriver...")
time.sleep(5)

# 2. 로그인하기.
print("Login...")
login_section = '//*[@id = "react-root"]/section/nav/div[2]/div/div/div[3]/div/span/a[1]/button'
driver.find_element_by_xpath(login_section).click()
time.sleep(4)
elem_login = driver.find_element_by_name("username")
elem_login.clear()
elem_login.send_keys('044apde@gmail.com')
elem_login = driver.find_element_by_name("password")
elem_login.clear()
elem_login.send_keys('skscjswo11')
elem_login.submit()
print("Accepted...")
time.sleep(4)

save_now_butotn = '//*[@id="react-root"]/section/main/div/div/div/section/div/button'
driver.find_element_by_xpath(save_now_butotn).click()

time.sleep(6)

driver.get(url)
time.sleep(3)

# 크롤링할 게시물의 수 지정하기
target = 5

# 크롤링할 게시물의 수.
num_of_data = target
print('Collecting a total of {0} data...'.format(target))
print("Collecting...")

time.sleep(3)

#4. 첫번째 게시글 열기.
select_first(driver)
time.sleep(3)

# 5. 비어있는 변수(result)만들기.
result = []

# 여러 게시물 크롤링하기.

for i in tqdm(range(target)):
    data = get_content(driver)
    result.append(data)
    move_next(driver)


# 데이터 수집완료 및 종료하기.
print("DATA SEARCH SUCCESS.")
print("SHUT DOWN CHROME IN 2 SECONDS")
time.sleep(2)

# 크롤링 후 엑셀에 저장한다.
instagram_crawling = pd.DataFrame(result, columns=['ID', 'Contents', 'Date', 'Like', 'Place', 'Tag'])
instagram_crawling.to_excel('instagram_crawling ' + str(now)[:13] + '.xlsx')

# Final_Data = pd.read_excel("/Users/044apde/Documents/GitHub/Code_Zero/K/insta.xlsx")
# Final_Data.head()
driver.close()