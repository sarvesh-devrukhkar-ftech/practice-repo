import requests
from bs4 import BeautifulSoup
import json

BASE_URL = "https://www.bbc.com"


def save_og_data(results):
    with open("bbc_data.json", "w", encoding="utf-8") as file:
        json.dump(results, file, indent=4, ensure_ascii=False)


def fetch_page(url):
    try:
        res = requests.get(url, timeout=10)

        if res.status_code == 200:
            print("\n===== START =====")
            print(f"Fetched: {url}")
            return res
        else:
            print(f"Error fetching {url}: {res.status_code}")
            return None

    except Exception as e:
        print(f"Request failed for {url} → {e}")
        return None


def parse_page(response):
    soup = BeautifulSoup(response.text, "html.parser")

    def get_og(tag_name):
        tag = soup.find("meta", property=tag_name)
        return tag["content"] if tag else "not found"

    og_data = {
        "title": get_og("og:title"),
        "description": get_og("og:description"),
        "image_url": get_og("og:image"),
        "image_alt": get_og("og:image:alt"),
    }


    next_urls = []
    all_links = soup.find_all("a", href=True)

    avoid = [
        "mailto:",
        "javascript:",
        "#",
        "/av/",
        "?page=",
        "?search=",
        "&sort=",
        "&filter=",
    ]

    for a in all_links:
        href = a["href"]

        if any(bad in href for bad in avoid):
            continue

        if "articles" in href:
            if href.startswith("/"):
                full_url = BASE_URL + href
            else:
                full_url = href
            next_urls.append(full_url)

    print("Parsed OG + URLs Successfully!")
    return next_urls, og_data

if __name__ == "__main__":
    frontier = [
        "https://www.bbc.com/",
        "https://www.bbc.com/news",
        "https://www.bbc.com/sport",
        "https://www.bbc.com/innovation",
        "https://www.bbc.com/business",
        "https://www.bbc.com/culture",
        "https://www.bbc.com/arts",
        "https://www.bbc.com/travel",
        "https://www.bbc.com/future-planet",
    ]
    visited = set()
    results = []

    MAX_PAGES = 100
    while frontier and len(visited) < MAX_PAGES:

        current_url = frontier.pop(0)

        if current_url in visited:
            continue

        visited.add(current_url)

        res = fetch_page(current_url)
        if not res:
            continue

        next_urls, og_data = parse_page(res)

        data_entry = {"url": current_url}
        data_entry.update(og_data)
        results.append(data_entry)

        save_og_data(results)

        print(f"Found {len(next_urls)} new URLs")

        for url in next_urls:
            if url not in visited:
                frontier.append(url)

        print("===== END =====\n")

    print("Crawling completed!")
    save_og_data(results)
    print("JSON saved: bbc_data.json")
