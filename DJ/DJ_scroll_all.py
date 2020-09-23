from bs4 import BeautifulSoup
import selenium.webdriver as webdriver
from urllib.parse import quote_plus
from urllib.request import urlopen

from time import sleep
import  csv
import time
import pandas as pd

driver = webdriver.Chrome(executable_path="../webdriver/chromedriver.exe")
url = "https://www.instagram.com/accounts/login/?source=auth_switcher"
driver.get(url)

time.sleep(3)
driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input').send_keys("")
driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[2]/div/label/input').send_keys("")
driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]/button/div').click()

search = input('태그를입력하세요 : ')
url = f'https://www.instagram.com/explore/tags/{quote_plus(search)}'  # 태그에 맞게 주소 변경

driver.get(url)
sleep(3)  # 로딩 시간을 위한 속도조절

SCROLL_PAUSE_TIME = 1.8  # 인스타게시물 스크롤 속도 조절 ( 1.0 ~ 2.0까지 사양에 맞게 조절 )

# Get scroll height
#last_height = driver.execute_script("return document.body.scrollHeight")
links =[]
while True:

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    insta = soup.select('.v1Nh3.kIKUG._bz0w')



    for i in insta[9:]:
        sup = i.a['href']
        link = 'https://www.instagram.com' + sup

        links.append(link)


        # Scroll down to bottom
    last_height = driver.execute_script("return document.body.scrollHeight")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    else: last_height = new_height
    continue




#중복제거
setlink = []
for first in links:
    if first not in setlink:
        setlink.append(first)
sub = []

result =[]
sol = int(input('스크롤할 갯수를 지정하세요 : '))

for i in setlink[:sol]:

    driver.get(i)

    time.sleep(5)
    sub = driver.page_source
    html= BeautifulSoup(sub,'html.parser')

    #id추적
    id1= html.select_one('a',{'class': 'sqdOP yWX7d     _8A5w5   ZIAjV  '})
    id2= id1.attrs['href']

    #게시날짜
    time1 = html.select_one('time', {"class": "FH9sR Nzb55"})
    time2 = time1.attrs['title']

    #좋아요수
    like = html.select('div.Nm9Fw > button')[0].text

    place = html.select('div.JF9hh')[0].text

    content = html.select('div.C4VMK > span')[0].text

    hashtag1 = html.find_all('a', {'class': 'xil3i'})
    hashtag = []
    for tag in hashtag1:
        has = str(tag).split("#")[1].split("</a>")[0]
        hashtag.append(has)

    sub = [id2, time2, like , place , content , hashtag ]

    result.append(sub)

Final = pd.DataFrame(result, columns=['id' , 'date', 'like', 'place', 'content', 'hashtag'])
Final.to_excel("스크롤.xlsx")

driver.close()
print('완료')
