import requests
from bs4 import BeautifulSoup
from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
keyword = "흑당버블티"
url = "https://www.instagram.com/explore/tags/{}/".format(keyword)
instagram_tags = []
instagram_tag_dates = []
driver = wd.Chrome("./chromedriver")
driver.get(url)
time.sleep(3)
driver.find_element_by_css_selector('div.v1Nh3.kIKUG._bz0w').click()
    for i in range(76086):
    time.sleep(1)
    try: data = driver.find_element_by_css_selector('.C7I1f.X7jCj') # C7I1f X7jCj tag_raw = data.text tags = re.findall('#[A-Za-z0-9가-힣]+', tag_raw) tag = ''.join(tags).replace("#"," ") # "#" 제거 tag_data = tag.split() for tag_one in tag_data: instagram_tags.append(tag_one) # print(instagram_tags) date = driver.find_element_by_css_selector("time.FH9sR.Nzb55" ).text # 날짜 선택 if date.find('시간') != -1 or date.find('일') != -1 or date.find('분') != -1: instagram_tag_dates.append('0주') else: instagram_tag_dates.append(date) #print(instagram_tag_dates) except: instagram_tags.append("error") instagram_tag_dates.append('error') try: WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a.HBoOv.coreSpriteRightPaginationArrow'))) driver.find_element_by_css_selector('a.HBoOv.coreSpriteRightPaginationArrow').click() except: driver.close() # date = datum2.text #print(date) time.sleep(3) driver.close()]z

