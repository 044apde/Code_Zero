from selenium import webdriver


driver = webdriver.Chrome(
    executable_path ="../webdriver/chromedriver"
)

url = "https://www.instagram.com/explore/tags/술담화/"
driver.get(url) # 엔터 치는 것
# driver.close()


