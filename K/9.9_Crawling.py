from urllib.request import urlopen # 인터넷 url을 열어주는 페키지
from urllib.parse import quote_plus # 한글을 유니코드 형식으로 변환
from bs4 import BeautifulSoup
from selenium import webdriver # webdriver 가져오기
import time # 크롤링 중 시간 대기를 위한 패키지
import warnings  # 경고메시지 제거 패키지
import selenium.webdriver.common.keys
from tqdm import tqdm
import pandas as pd
from requests import Request
from flask import Request
import re # 문자열에서 숫자만 뽑아 내는 라이브러리.


warnings.filterwarnings(action='ignore') # 경고 메세지 제거

# 인스타그램 url 생성
baseUrl = "https://www.instagram.com/explore/tags/"
plusUrl = input("검색할 태그를 입력하세요 : ")
url = baseUrl + quote_plus(plusUrl)

print("Chrome Driver를 실행합니다.")
driver = webdriver.Chrome(
    executable_path = "./ChromeDriver/chromedriver"
)

driver.get(url)

time.sleep(4)

# 로그인하기
login_section = '//*[@id = "react-root"]/section/nav/div[2]/div/div/div[3]/div/span/a[1]/button'
driver.find_element_by_xpath(login_section).click()
time.sleep(3)

elem_login = driver.find_element_by_name("username")
elem_login.clear()
elem_login.send_keys('044apde@gmail.com')

elem_login = driver.find_element_by_name("password")
elem_login.clear()
elem_login.send_keys('skscjswo11')
elem_login.submit()

time.sleep(4)

save_now_butotn = '//*[@id="react-root"]/section/main/div/div/div/section/div/button'
driver.find_element_by_xpath(save_now_butotn).click()

time.sleep(4)

# 총 게시물 숫자 불러오기
pageString = driver.page_source
bsObj = BeautifulSoup(pageString, 'lxml')
temp_data = bsObj.find_all(name='meta')[-1]
temp_data = str(temp_data)
start = temp_data.find('게시물') + 4
end = temp_data.find('개')
total_data = temp_data[start:end]
total_data = str(total_data)
total_data = re.findall('\d+', total_data)
print("총 '{0}'개의 게시물이 검색되었습니다.".format(total_data[0] + total_data[1]))

# [HashTag Crawling]

# 스크롤 내리
print("게시물을 수집하는 중입니다.")
SCROLL_PAUSE_TIME = 1.3
reallink = []

while True: # break 될 때까지 무한 반복한다.
    pageString = driver.page_source
    soup = BeautifulSoup(pageString, 'lxml')

    for link1 in soup.find_all(name = 'div', attrs={"class" : "Nnq7C weEfm"}):
        for i in range(3):
            title = link1.select('a')[i] # class" : Nnq7c weEfm 에서 a 를 순서대로 3개 챶는다.
            real = title.attrs['href'] #  href가 real로 로 들어간다.
            reallink.append(real) # real이 reallink로 들어간다.

    last_height = driver.execute_script('return document.body.scrollHeight') # last_height는 scrollheight이다.
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") # 0에서 scrollheight만큼 내린다.
    time.sleep(SCROLL_PAUSE_TIME) # 멈춘다 SCROLL_PASUSE_TIME 만큼
    new_height = driver.execute_script("return document.body.scrollheight") # new_height는 scrollheight만큼 내린 것이다.

    if new_height == last_height: # 두 height가 같다면,
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") # 스크롤을 내린다.
        time.sleep(SCROLL_PAUSE_TIME) # 멈춘다.
        new_height = drvier.execute_script("return document.body.scrollHeight") # new_height는 스크롤을 내린 값이다.
        print(new_height)

        if new_height > 100 : # 스크롤 내린 hight가 new_height와 같다면, break한다.
            break # 무한 반복을 멈춘다.
        else:
            last_height = new_height # 그렇지 않다면, new_height가 last_heifht가 되고, 한번 더 진행한다.
            continue
    time.sleep(0.5)

# 데이터 가져오기
num_of_data = len(reallink)
print('총 {0}개의 데이터를 수집합니다.'.format(num_of_data))

csvtext = []

for i in tqdm(range(num_of_data)):

    csvtext.append([])
    req = Request("https://www.instagram.com/p" + reallink[i], headers={'User-Agent': 'Mozila/5.0'})

    webpage = urlopen(req).read()
    soup = BeautifulSoup(webpage, 'lxml', from_encoding='utf-8')
    soup1 = soup.find('meta', attrs={'property': "og:description"})

    reallink1 = soup1['content']
    reallink1 = reallink1[reallink1.find("@") + 1:reallink1.find(")")]
    reallink1 - reallink1[:20]

    if reallink1 == '':
        reallink1 = "NULL"
    csvtext[i].append(hashtags)

# write to csv

data = pd.DataFrame(csvtext)
data.to_csv('insta.xtx', encoding = 'utf-8')

driver.close()


