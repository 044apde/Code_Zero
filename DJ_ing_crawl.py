from urllib.request import urlopen
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from selenium import webdriver
import time

baseurl = 'https://www.instagram.com/explore/tags/'
plusurl = input('검색할태그를 입력하세요 : ' )
url = baseurl+ quote_plus(plusurl)

driver=webdriver.Chrome(executable_path="../webdriver/chromedriver.exe")
driver.get(url)

time.sleep(5)

html =driver.page_source
soup= BeautifulSoup(html,"html.parser")

insta =soup.select('.v1Nh3.kIKUG._bz0w')#원하는 태그안에 있는 정보를 가져와서 저장, 다가져온거임
# 프로그램 동작 오류시 htmlpaser, lxml 설치


n=1
for i in insta: #insta에 있는 이미지를 순차적으로 가져올것임
    print('https://www.instagram.com'+ i.a['href']) #주소 프린트
    imgurl = i.select_one('.KL4Bh').img['src'] # 지정 주소에서 class명 kl4bh를 가져오기.그중 src를 가져옴
    with urlopen(imgurl) as f:
        with open('./img/'+ plusurl + str(n)+'.jpg','wb') as h: #w는 텍스트파일 이미지는 wb
            img =f.read(
            ) #url오픈한걸 읽어라
            h.write(img)

    n += 1
    print(imgurl)
    print()





## 셀레니움을 쓰는 용도

