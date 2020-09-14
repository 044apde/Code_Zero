from urllib.request import urlopen, Request
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import warnings
from tqdm import tqdm
import pandas as pd


warnings.filterwarnings(action='ignore')

baseUrl = "https://www.instagram.com/explore/tags/"
plusUrl = input('검색할 태그를 입력하세요 : ')
url = baseUrl + quote_plus(plusUrl)

print("Chrome Driver를 실행합니다.")
driver = webdriver.Chrome(
    executable_path="./ChromeDriver/chromedriver"
)
driver.get(url)
time.sleep(3)


# 로그인 하기
login_section = '//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/span/a[1]/button'
driver.find_element_by_xpath(login_section).click()
time.sleep(3)


elem_login = driver.find_element_by_name("username")
elem_login.clear()
elem_login.send_keys('044apde@gmail.com')

elem_login = driver.find_element_by_name('password')
elem_login.clear()
elem_login.send_keys('skscjswo11')
elem_login.submit()
time.sleep(3)

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
print("총 {0}개의 게시물이 검색되었습니다.".format(total_data))

"""태그 크롤링"""
print("게시물을 수집하는 중입니다.")

SCROLL_PAUSE_TIME = 1.0
reallink = []

while True:
    pageString = driver.page_source
    bsObj = BeautifulSoup(pageString, 'lxml')

    for link1 in bsObj.find_all(name='div', attrs={"class":"Nnq7C weEfm"}):
        for i in range(3):
            title = link1.select('a')[i]
            real = title.attrs['href']
            reallink.append(real)

    last_height = driver.execute_script('return document.body.scrollHeight')
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(SCROLL_PAUSE_TIME)
    new_height = driver.execute_script("return document.body.scrollHeight")

    if new_height == last_height:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            break
        else:
            last_height = new_height
            continue
    # 게시물의 개수가 계속 바뀌거나 전체 게시물을 가져오지 못한다면
    # 아래 time.sleep의 시간(초)을 늘려주세요.
    time.sleep(2)


# 전체 데이터 및 데이터 배치 사이즈 나누기
num_of_data = len(reallink)
batch_size = 100
num_batch = num_of_data // batch_size + 1

print("검색된 {0}개의 게시물 중 {1}개의 게시물을 가지고오는데 성공하였습니다.".format(total_data, num_of_data))
print('총 {0}개의 데이터를 수집합니다.'.format(num_of_data))

## 해시태그 가져오기
csvtext = []

for batch in range(num_batch):
    print('{1}개 중 {0} 번째 batch 입니다.'.format(batch+1, num_batch))
    if batch == num_batch:
        for i in tqdm(range(batch * batch_size, num_of_data)):
            csvtext.append([])
            req = Request("https://www.instagram.com/p"+reallink[i], headers={'User-Agent': 'Mozila/5.0'})

            webpage = urlopen(req).read()
            soup = BeautifulSoup(webpage, 'lxml', from_encoding='utf-8')
            soup1 = soup.find('meta', attrs={'property':"og:description"})

            reallink1 = soup1['content']
            reallink1 = reallink1[reallink1.find("@") + 1:reallink1.find(")")]
            reallink1 = reallink1[:20]

            if reallink1 == '':
                reallink1 = "Null"
            csvtext[i].append(reallink1)

            for reallink2 in soup.find_all('meta', attrs={'property':"instapp:hashtags"}):
                hashtags = reallink2['content'].rstrip(',')
                csvtext[i].append(hashtags)

            time.sleep(0.5)
    else:
        for i in tqdm(range(batch * batch_size, (batch+1) * batch_size)):
            csvtext.append([])
            req = Request("https://www.instagram.com/p"+reallink[i], headers={'User-Agent': 'Mozila/5.0'})

            webpage = urlopen(req).read()
            soup = BeautifulSoup(webpage, 'lxml', from_encoding='utf-8')
            soup1 = soup.find('meta', attrs={'property':"og:description"})

            reallink1 = soup1['content']
            reallink1 = reallink1[reallink1.find("@") + 1:reallink1.find(")")]
            reallink1 = reallink1[:20]

            if reallink1 == '':
                reallink1 = "Null"
            csvtext[i].append(reallink1)

            for reallink2 in soup.find_all('meta', attrs={'property':"instapp:hashtags"}):
                hashtags = reallink2['content'].rstrip(',')
                csvtext[i].append(hashtags)

            time.sleep(0.5)
    time.sleep(3)

data = pd.DataFrame(csvtext)
data.to_csv('insta.txt', encoding='utf-8')

# driver.close()
