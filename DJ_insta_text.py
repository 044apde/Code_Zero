import csv
import time
from urllib.parse import quote_plus
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from openpyxl import Workbook



driver=webdriver.Chrome(executable_path="../webdriver/chromedriver.exe")
url = "https://www.instagram.com/accounts/login/?source=auth_switcher"
driver.get(url)

time.sleep(3)
driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input').send_keys("")
driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[2]/div/label/input').send_keys("")
driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]/button/div').click()

search=input('태그를입력하세요 : ')
url = f'https://www.instagram.com/explore/tags/{quote_plus(search)}' #태그에 맞게 주소 변경


driver.get(url)

#스크롤하기

driver.execute_script("window.sc")


time.sleep(3)

elem = driver.find_element_by_class_name('EZdmt')
div = elem.find_elements_by_class_name('_bz0w')
action = ActionChains(driver)

xlsx = Workbook()
sheet = xlsx.active
sheet.append(['글내용', '좋아요'])

for post in div:

    action.reset_actions()
    action.move_to_element(post)
    action.click()
    action.perform()

    time.sleep(5)

    first = driver.find_element_by_class_name('CkGkG')
    second = first.find_element_by_class_name('zZYga')
    thd = second.find_element_by_class_name('s2MYR')
    ft = thd.find_element_by_class_name('eo2As ')
    source = ft.find_element_by_class_name('C4VMK')
    love = ft.find_element_by_class_name('Nm9Fw')

    #hashtag = second.get_attribute('href')
    #hashtags=[]
    #for i in hashtag:
    #    hashtags.append(i)



    sheet.append([source.text,love.text])

    action.reset_actions()
    action.send_keys(Keys.ESCAPE)
    action.perform()

    time.sleep(1)

driver.quit()

file_name = '술담화.xlsx'
xlsx.save(file_name)



print('완료되었습니다.')










