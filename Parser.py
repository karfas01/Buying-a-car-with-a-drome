from bs4 import BeautifulSoup
import requests
import json
import os
import re

if not os.path.exists("media"):
    os.makedirs("media")
if not os.path.exists('json_database'):
    os.makedirs('json_database')

url = "https://auto.drom.ru/region78/"
payload = {"unsold": 1}
response = requests.get(url, params=payload)
soup = BeautifulSoup(response.text, "html.parser")

car_data_by_brand = {}
cars = soup.find_all("a", class_="css-4zflqt e1huvdhj1")

def download_image(image_url, brand):
    image_path = f"media/{brand}-{brand}.jpg"
    with open(image_path, "wb") as file:
        image_response = requests.get(image_url)
        file.write(image_response.content)

for car in cars:
    brand_div = car.find(class_="css-16kqa8y e3f4v4l2")
    full_brand = brand_div.text.strip().split()
    save_brend = brand_div.text.strip()
    brand = full_brand[0]

    image_url = car.find(class_="css-9w7beg evrha4s0")["src"]

    price_full = car.find(class_='css-46itwz e162wx9x0')
    price_str = price_full.text.strip()
    price = re.sub(r'\D', '', price_str)

    if brand in car_data_by_brand:
        car_data_by_brand[brand].append({
            "title": f"Ad {save_brend}",
            "image_url": image_url,
            "price": price
        })
    else:
        car_data_by_brand[brand] = [{
            "title": f"Ad {save_brend}",
            "image_url": image_url,
            "price": price
        }]
    
    download_image(image_url, brand)

    json_file_path = f"json_database/{brand}_data.json"
    with open(json_file_path, "w") as json_file:
        json.dump(car_data_by_brand[brand], json_file, indent=4)