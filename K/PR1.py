import requests
from bs4 import BeautifulSoup

instagram_result = requests.get("https://www.instagram.com/explore/tags/%EC%88%A0%EB%8B%B4%ED%99%94/")

# print(instagram_result.text) # 모든 html 가져오기

instagram_soup = BeautifulSoup(instagram_result.text, "html.parser")

# print(instagram_soup)

# print(instagram_soup.title) # bring the title

# pagination = instagram_soup.find("div", {"class" : "pagination"}) # 쪽수 매기기

# print(pagination)




