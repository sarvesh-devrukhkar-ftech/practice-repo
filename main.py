import requests
from bs4 import BeautifulSoup
import json
import re


def fetch_page(url):
    response = requests.get(url)

    if response.status_code == 200:
        return response
    else:
        print("failed to fetched data")


def parse_page(response):
    if response is None:
        return None
    soup = BeautifulSoup(response.text, "html.parser")
    return soup

def parse_next_urls(soup):
    if soup is None:
        return [],

    next_urls = []

    
    links = soup.find_all("a", href=True)

    def get_og(tag_name):
        tag = soup.find("meta", property=tag_name)
        return tag.get("content") if tag else "not found"
    

    og_all_data = {
        "og_title": get_og("og:title"),
        "og_description": get_og("og:description"),
        "image_url": get_og("og:image"),
        "image_url_alt": get_og("og:image:alt"),
    }

    print("OG Title:", og_all_data["og_title"])
    print("OG Description:", og_all_data["og_description"])
    print("OG Image URL:", og_all_data["image_url"])
    print("OG Image Alt Text:", og_all_data["image_url_alt"])
    print("---------------------------------------------------")


    candidiates = ["#", "javascript:", "mailto:"]
    for link in links:
        href = link["href"]

        skip = False
        for item in candidiates:
            if href.startswith(item):
                skip = True
                break
        if skip:
            continue

        if re.search("articles", href):
            if href.startswith("/"):
                next_urls.append("https://www.bbc.com" + href)
            else:
                next_urls.append(href)

    return next_urls, og_all_data

def json_file(filee):
    with open("crawler.json", "w") as file:
        json.dump(list(filee), file, indent=4)

frontier = [
    "https://www.bbc.com/news",
    "https://www.bbc.com/sport",
    "https://www.bbc.com/business",
]
visited = {} 
results = list()

while len(frontier) > 0:
    current_url = frontier.pop(0)
    if current_url in visited:
        continue
    response = fetch_page(current_url)
    soup = parse_page(response)
    next_urls, og_all_data  = parse_next_urls(soup)
    url = parse_next_urls
    frontier.extend(next_urls)
    visited[current_url] = ""
    print(f"Visited on : {current_url} | Found: {len(next_urls)} links")


    results.append(og_all_data)

    json_file(results)