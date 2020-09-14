# Library
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
from urllib import request
import re # 문자열에서 숫자만 뽑아 내는 라이브러리.


warnings.filterwarnings(action='ignore') # 경고 메세지 제거

# 인스타그램 url 생성
baseUrl = "https://www.instagram.com/explore/tags/"
plusUrl = input("Enter the tag to search : ")
url = baseUrl + quote_plus(plusUrl)

print("Excute Chrome Driver...")
driver = webdriver.Chrome(
    executable_path = "./ChromeDriver/chromedriver"
)

driver.get(url)

time.sleep(5)

# 로그인하기
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

# 총 게시물 숫자 불러오기
print("Find posting...")
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

# 스크롤 내리기기
print("게시물을 수집하는 중입니다...")
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

    # last_height = driver.execute_script('return document.body.scrollHeight') # last_height는 scrollheight이다.
    # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") # 0에서 scrollheight만큼 내린다.
    # time.sleep(SCROLL_PAUSE_TIME) # 멈춘다 SCROLL_PASUSE_TIME 만큼
    # new_height = driver.execute_script("return document.body.scrollheight") # new_height는 scrollheight만큼 내린 것이다.
    # print("데이터 수집 준비중...")
    # time.sleep(3)

    break

    # if new_height == last_height: # 두 height가 같다면,
    #     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") # 스크롤을 내린다.
    #     time.sleep(SCROLL_PAUSE_TIME) # 멈춘다.
    #     new_height = drvier.execute_script("return document.body.scrollHeight") # new_height는 스크롤을 내린 값이다.
    #
    #
    #     if new_height == new_height : # 스크롤 내린 hight가 new_height와 같다면, break한다.
    #         break # 무한 반복을 멈춘다.
    #     else:
    #         last_height = new_height # 그렇지 않다면, new_height가 last_heifht가 되고, 한번 더 진행한다.
    #         continue
    #     print(last_height)
    # time.sleep(0.5)



# 데이터 가져오기

num_of_data = len(reallink)
print('총 {0}개의 데이터를 수집합니다.'.format(num_of_data))

csvtext = []

for i in tqdm(range(num_of_data - 30)):

    csvtext.append([])

    Post_link = 'https://www.instagram.com' + reallink[i]
    driver.get(Post_link)
    time.sleep(2)

    webpage = driver.page_source
    soup = BeautifulSoup(webpage, 'html.parser')

    # User_ID = soup.select('a', {'class :Jv7Aj  MqpiF  '})
    # print(User_ID)
    hash_tag = soup.find_all('a',{'class' : 'xil3i'})
    # Time = soup.find('a', {'class :_7UhW9  PIoXz       MMzan   _0PwGv         uL8Hv         '})
    # print(Time)
    # Collect_User_ID = []
    # Collect_Time = []
    Collect_hash_tag = []

    # Collect_User_ID.append(User_ID)
    # Collect_Time.append(Time)
    Collect_hash_tag.append(hash_tag)

All_Data = []
# All_Data = All_Data.append(Collect_Time)
All_Data = All_Data.append(Collect_hash_tag)
# All_Data = All_Data.append(Collect_User_ID)

# write to csv
All_Data = pd.DataFrame(All_Data)
data = pd.DataFrame(All_Data)
print(data)
data.to_csv("insta.txt")

driver.close()


