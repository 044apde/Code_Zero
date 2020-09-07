from selenium import webdriver
import time
from bs4 import BeautifulSoup
import urllib.request
import os

driver = webdriver.Chrome("./ChromeDriver/chromedriver")

driver.get('https://www.instagram.com/accounts/login/?source=auth_switcher')

time.sleep(3) #웹 페이지 로드를 보장하기 위해 3초 쉬기

#

id = 'cranberrygame@yahoo.com'
password = ''
id_input = driver.find_elements_by_css_selector('#react-root > section > main > div > article > div > div > div > form > div > div > label > input')[0]
id_input.send_keys(id)
password_input = driver.find_elements_by_css_selector('#react-root > section > main > div > article > div > div > div > form > div > div > label > input')[1]
password_input.send_keys(password)
password_input.submit()

time.sleep(3)

#

driver.get('https://www.instagram.com/explore/tags/게임')

time.sleep(3)

#

text = driver.page_source
#print(text)

soup = BeautifulSoup(text, 'html.parser')

for div in soup.select('div.v1Nh3.kIKUG._bz0w'):
    #url = 'https://www.instagram.com' + div.a['href']
    image_url = div.img['src']
    #print(url, image_url)

    #print(image_url) #https://instagram.ficn6-1.fna.fbcdn.net/v/t51.2885-15/e35/c236.0.608.608a/81887242_134904677995894_2593890246933116496_n.jpg?_nc_ht=instagram.ficn6-1.fna.fbcdn.net&_nc_cat=110&_nc_ohc=PyFoOauFOggAX_qoFU8&oh=29c19b7ff0fb0c2b13304279f77566d7&oe=5ED361DB
    file_name = image_url[image_url.rindex('/')+1:]
    file_name = file_name[:file_name.index('?')]
    print(file_name)
    folder = '게임'
    if not os.path.exists(folder):
        os.makedirs(folder)
    urllib.request.urlretrieve(image_url, folder + '/' + file_name)

#driver.quit()