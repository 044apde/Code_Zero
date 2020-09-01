from libs.instagram_crawl import crawl

url = "https://www.instagram.com/explore/tags/술담화/"

pageSring = crawl(url)
print(pageSring)