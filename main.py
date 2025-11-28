import requests
from bs4 import BeautifulSoup
import json
def fetch_page(current_url):
    try:
        response = requests.get(current_url, timeout=5)
        if response.status_code == 200:
            return response
        else:
            print(f"Error fetching {current_url}: {response.status_code}")
            return None
    except Exception as e:
        print(f"Request failed for {current_url}: {e}")
        return None


def parse_page(response):
    if response is None:
        return None
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup


def parse_next_urls(parsed_data):
    if parsed_data is None:
        return []

    next_urls = []
    links = parsed_data.find_all('a', href=True)
    
    head_list=[]
    head_data = parsed_data.find_all('h2')

    for link in links:
        href = link['href']

        if href.startswith("#") or href.startswith("javascript:") or href.startswith("mailto:"):
            continue
        # if not href.startswith(current_url):
        #     continue
        if href.startswith("/"):
            href = "https://www.bbc.com" + href

        next_urls.append(href)
        for head in head_data:
            head_list.append(head.get_text())
            
        for i in range (Limit):
            data= {
            "url": next_urls
            ,"headlines": head_list
         }
        with open("bbc_page.json", "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
    
    #print("JSON saved successfully to bbc_page.json")
    return next_urls




frontier = [
      'https://www.bbc.com/'
    # 'https://www.bbc.com/news'
#     'https://www.bbc.com/sport',
#     'https://www.bbc.com/innovation',
#     'https://www.bbc.com/business',
#     'https://www.bbc.com/culture',
#     'https://www.bbc.com/arts',
#     'https://www.bbc.com/travel',
#     'https://www.bbc.com/future-planet'
         ]
visited = {}

while len(frontier) > 0:

    try:
        current_url = frontier.pop(0)
    except IndexError:
        break

    if current_url in visited:
        continue
    else:
        response = fetch_page(current_url)
        parsed_data = parse_page(response)
        next_urls = parse_next_urls(parsed_data)
        frontier.extend(next_urls)
        visited[current_url] = ""

    # print(f"Visited: {current_url} | Found: {len(next_urls)} links")
