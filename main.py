
import requests
from bs4 import BeautifulSoup


def fetch_page(url):
    response = requests.get(url)

    if response.status_code == 200:
        return response
    else:
        print("failed to fetched data")

MAX_ITEMS = 50

def parse_page(response):
    return BeautifulSoup(response.text, "html.parser")


def parse_next_urls(parsed_data):
    if parsed_data is None:
        return []

    next_urls = []
    links = parsed_data.find_all("a", href=True)

    for title in parsed_data.find_all("h2"):
        if(title.string):
            print("heading-----",title.get_text())
            
    

    for link in links:
        href = link["href"]

        if href.startswith("#"):
            continue
        if href.startswith("javascript:"):
            continue
        if href.startswith("mailto:"):
            continue
        if href.startswith("/"):
            href = "https://www.bbc.com" + href

        next_urls.append(href)

    return next_urls


frontier = [
    "https://www.bbc.com/news",
    "https://www.bbc.com/sport",
    "https://www.bbc.com/business",
]
visited = {}

while len(frontier) > 0:
    current_url = frontier.pop(0)
    if current_url in visited:
        continue
    response = fetch_page(current_url)
    parsed_data = parse_page(response)
    next_urls = parse_next_urls(parsed_data)
    frontier.extend(next_urls)
    visited[current_url] = ""
    print(f"Visited on : {current_url} | Found: {len(next_urls)} links")




