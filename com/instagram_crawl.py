import requests

def crawl(url):
    data = requests.get(url)
    print(data, url)
    return data.content

url = "https://www.instagram.com/explore/tags/술담화/"

pageSring = crawl(url)
print(pageSring)