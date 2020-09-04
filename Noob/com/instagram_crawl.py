from Noob.libs.instagram_crawl import crawl

url = "https://www.instagram.com/explore/tags/술담화/"

pageString = crawl(url)
print(pageString)