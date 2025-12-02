import requests
from bs4 import BeautifulSoup
import json


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
        return []

    next_urls = []

    
    links = soup.find_all("a", href=True)


    title_tag = soup.find('meta', property="og:title")
    if title_tag:
        og_title = title_tag.get("content")
    else:
        og_title = "not found"

    description_tag = soup.find('meta', property="og:description")
    if description_tag:
        og_description = description_tag.get("content")
    else:
        og_description = "not found"

    image_tag = soup.find('meta', property="og:image")
    if image_tag:
        og_image = image_tag.get("content")
    else:
        og_image = "not found"

    image_alt_tag = soup.find('meta', property="og:image:alt")
    if image_alt_tag:
        og_image_alt = image_alt_tag.get("content")
    else:
        og_image_alt = "not found"

    print("OG Title:", og_title)
    print("OG Description:", og_description)
    print("OG Image URL:", og_image)
    print("OG Image Alt Text:", og_image_alt)
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
results =[]

while len(frontier) > 0:
    current_url = frontier.pop(0)
    if current_url in visited:
        continue
    response = fetch_page(current_url)
    soup = parse_page(response)
    next_urls = parse_next_urls(soup)
    url = parse_next_urls
    frontier.extend(next_urls)
    visited[current_url] = ""
    print(f"Visited on : {current_url} | Found: {len(next_urls)} links")


    results={
    "url": next_urls,
    # "title": og_title,
    # "description": og_description,
    # "image": og_image,
    # "image_alt": og_image_alt
      }


    with open("crawler_test.json", "w", encoding="utf-8") as file:
        json.dump(results, file, indent=4, ensure_ascii=False)
