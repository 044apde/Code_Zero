from selenium import webdriver


driver = webdriver.Chrome(
    executable_path = "../webdriver/chromedriver"
)

url = "https://www.instagram.com/explore/tags/%EC%88%A0%EB%8B%B4%ED%99%94/"
driver.get(url)
