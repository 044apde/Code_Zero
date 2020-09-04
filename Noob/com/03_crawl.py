from selenium import webdriver
from time import sleep
driver = webdriver.Chrome(
    executable_path="../webdriver/chromedriver"
)

url = "https://www.instagram.com/explore/tags/술담화/"
driver.get(url) # 주소입력하고 엔터
sleep(5)
pageString = driver.page_source
print(pageString)

# instagram cover 껍대기

# instagram contents 내용 <div class="RnEpo  _Yhr4">

# driver.close()