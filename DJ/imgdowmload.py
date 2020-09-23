from bs4 import BeautifulSoup
import selenium.webdriver as webdriver
from urllib.parse import quote_plus
from urllib.request import urlopen

from time import sleep
import  csv
import time

driver = webdriver.Chrome(executable_path="../webdriver/chromedriver.exe")
url = "https://www.instagram.com/accounts/login/?source=auth_switcher"
driver.get(url)

time.sleep(3)
driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input').send_keys("dong_8_2_ya")
driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[2]/div/label/input').send_keys("dusrud110204~")
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
        imgUrl = i.select_one('.KL4Bh').img['src']
        links.append(imgUrl)



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

setlink = []
for first in links:
    if first not in setlink:
        setlink.append(first)

n=1
for ses in setlink:
    with urlopen(ses) as asd:
        with open('./imgfile/' + search + str(n) + '.jpg', 'wb') as efg:
            img = asd.read()
            efg.write(img)
    n += 1
