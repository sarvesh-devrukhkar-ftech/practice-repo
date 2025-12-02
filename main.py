# import requests
# from bs4 import BeautifulSoup
# import json

# def fetch_page(current_url):
    
#     response = requests.get(current_url, timeout=30)
#     if response.status_code == 200:
#         return response
#     else:
#         print(f"Error fetching {current_url}: {response.status_code}")
#         return None

# def parse_page(response):
#     if response is None:
#         return None
#     soup = BeautifulSoup(response.text, 'html.parser')
#     return soup


# def parse_next_urls(parsed_data):
#     if parsed_data is None:
#         return []
#     next_urls = []
#     links = parsed_data.find_all('a', href=True)
    
#     # head_list=[]
#     # head_data = parsed_data.select("meta[property='og:title']")
#     for link in links:
#         href = link['href']

#         # if href.startswith("#") or href.startswith("javascript:") or href.startswith("mailto:"):
#         #     continue
        
#         # if href.startswith("/"):
#         #     href = "https://www.bbc.com" + href
#         if not href.startswith("https://www.bbc.com"):
#             continue
#         next_urls.append(href)
#     next_urls = list(set(next_urls))  # Remove duplicates
#     # print("JSON saved successfully to bbc_page.json")
#     return next_urls

# # for head in head_data:
# #             head_list.append(head['content'])
            
# #         for i in range (Limit):
# #             data= {
# #             "url": next_urls
# #             ,"headlines": head_list
# #          }
# #         with open("bbc_page.json", "w", encoding="utf-8") as file:
# #             json.dump(data, file, indent=4, ensure_ascii=False)



# def parse_head(parsed_data):
#     if parsed_data is None:
#         return None

#     head_list=[]
#     head_data = parsed_data.select("meta[property='og:title']")
#     for head in head_data:
#         head_list.append(head['content'])
#     return head_list

# def parse_description(parsed_data):
#     if parsed_data is None:
#         return None

#     description_list=[]
#     description_data = parsed_data.select("meta[name='description']")
#     for desc in description_data:
#         description_list.append(desc['content'])
#     return description_list

# def parse_image(parsed_data):
#     if parsed_data is None:
#         return None
#     image_list=[]
#     image_data = parsed_data.select("meta[property='og:image']")
#     for img in image_data:
#         image_list.append(img['content'])
#     return image_list

# def parse_image_alt(parsed_data):
#     if parsed_data is None:
#         return None

#     image_alt_list=[]
#     image_alt_data = parsed_data.select("meta[property='og:image:alt']")
#     for img_alt in image_alt_data:
#         image_alt_list.append(img_alt['content'])
#     return image_alt_list

# # def save_json(next_urls, headlines,filename):
# #     for i in range (100 ):
# #         data= {
# #             "url": next_urls
# #             ,"headlines": headlines
# #          }
# #     with open(filename, 'w') as f:
# #         json.dump(data, f, indent=4)    
        
# if __name__ == "__main__":
#     frontier = [
#     'https://www.bbc.com/',
#     'https://www.bbc.com/news',
#     'https://www.bbc.com/sport',
#     'https://www.bbc.com/innovation',
#     'https://www.bbc.com/business',
#     'https://www.bbc.com/culture',
#     'https://www.bbc.com/arts',
#     'https://www.bbc.com/travel',
#     'https://www.bbc.com/future-planet'
#          ]
#     visited = {}
#     # results = []

#     while len(frontier) > 0:
#         current_url = frontier.pop(0)

#         if current_url in visited:
#             continue
    
#         response = fetch_page(current_url)
#         parsed_data = parse_page(response)
#         next_urls = parse_next_urls(parsed_data)
#         headlines = parse_head(parsed_data)
#         description=parse_description(parsed_data)
#         image=parse_image(parsed_data)
#         image_alt=parse_image_alt(parsed_data)
#         # save=save_json(next_urls,headlines,"bbc_page.json")
#         frontier.extend(next_urls)
#         visited[current_url] = ""
#         for total_data in range(100):
#             print(f"Visited: {current_url} | Found: {len(next_urls)} links")
#             print(f"Headlines: {headlines}")
#             print(f"Description: {description}")
#             print(f"Image URLs: {image}")
#             print(f"Image Alts: {image_alt}")
#             print ("--------------------------------------------------")
#         # data= {
#         #         "url": next_urls,
#         #         "headlines": headlines,
#         #         "description": description,
#         #         "image_urls": image,
#         #         "image_alts": image_alt
#         #      }
#         # results.append(data)
#         # with open("bbc_page.json", 'w') as f:
#         #     json.dump(results, f, indent=4)  


import requests
from bs4 import BeautifulSoup
import json

def fetch_page(current_url):
    
    response = requests.get(current_url, timeout=30)
    if response.status_code == 200:
        return response
    else:
        print(f"Error fetching {current_url}: {response.status_code}")
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
    
    for link in links:
        href = link['href']

        if not href.startswith("https://www.bbc.com"):
            continue

        next_urls.append(href)

    return next_urls


def parse_head(parsed_data):
    if parsed_data is None:
        return None

    head_list=[]
    head_data = parsed_data.select("meta[property='og:title']")
    for head in head_data:
        head_list.append(head['content'])
    return head_list

def parse_description(parsed_data):
    if parsed_data is None:
        return None

    description_list=[]
    description_data = parsed_data.select("meta[name='description']")
    for desc in description_data:
        description_list.append(desc['content'])
    return description_list

def parse_image(parsed_data):
    if parsed_data is None:
        return None
    image_list=[]
    image_data = parsed_data.select("meta[property='og:image']")
    for img in image_data:
        image_list.append(img['content'])
    return image_list

def parse_image_alt(parsed_data):
    if parsed_data is None:
        return None

    image_alt_list=[]
    image_alt_data = parsed_data.select("meta[property='og:image:alt']")
    for img_alt in image_alt_data:
        image_alt_list.append(img_alt['content'])
    return image_alt_list


if __name__ == "__main__":
    frontier = [
        'https://www.bbc.com/',
        'https://www.bbc.com/news',
        'https://www.bbc.com/sport',
        'https://www.bbc.com/innovation',
        'https://www.bbc.com/business',
        'https://www.bbc.com/culture',
        'https://www.bbc.com/arts',
        'https://www.bbc.com/travel',
        'https://www.bbc.com/future-planet'
    ]

    visited = {}
    

    results = []

  
    max_pages = 200
    max_depth = 3

    new_frontier = []
    for url in frontier:
        new_frontier.append((url, 0))

    frontier = new_frontier

    while len(frontier) > 0 and len(results) < max_pages:
        current_url, depth = frontier.pop(0)

        if current_url in visited or depth > max_depth:
            continue

        response = fetch_page(current_url)
        parsed_data = parse_page(response)
        next_urls = parse_next_urls(parsed_data)
        headlines = parse_head(parsed_data)
        description = parse_description(parsed_data)
        image = parse_image(parsed_data)
        image_alt = parse_image_alt(parsed_data)

        for url in next_urls:
            frontier.append((url, depth + 1))

        visited[current_url] = True

        print(f"Visited: {current_url} | Found: {len(next_urls)} links")
        print(f"Headlines: {headlines}")
        print(f"Description: {description}")
        print(f"Image URLs: {image}")
        print(f"Image Alts: {image_alt}")
        print("--------------------------------------------------")

        page_data = {
            "url": current_url,
            "next_urls": next_urls,
            "headlines": headlines,
            "description": description,
            "image_urls": image,
            "image_alts": image_alt
        }

        results.append(page_data)


    with open("bbc_page.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)

    print("JSON saved successfully!")
