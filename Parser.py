from bs4 import BeautifulSoup
import requests
import json
import os
import re

if not os.path.exists("media"):
    os.makedirs("media")
if not os.path.exists('json_database'):
    os.makedirs('json_database')

urls = ["https://auto.drom.ru/region78/", "https://auto.drom.ru/region78/page2/", "https://auto.drom.ru/region78/page3/"]
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}
payload = {"unsold": 1,
           "ph": 1}
car_data_by_brand = {}


def download_image(image_url, save_brand):
    image_path = f"media/{save_brand}.jpg"
    with open(image_path, "wb") as file:
        image_response = requests.get(image_url)
        file.write(image_response.content)
    return image_path


for url in urls:
    response = requests.get(url, params=payload, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    cars = soup.find_all("a", class_="css-4zflqt e1huvdhj1")

    for car in cars:
        brand_div = car.find(class_="css-16kqa8y e3f4v4l2")
        full_brand = brand_div.text.strip().split()
        save_brand = brand_div.text.strip()
        brand = full_brand[0]

        image_url = car.find(class_="css-9w7beg evrha4s0")["src"]

        price_full = car.find(class_="css-46itwz e162wx9x0")
        price_str = price_full.text.strip()
        price = re.sub(r'\D', '', price_str)

        all_car_info = car.find(class_="css-1fe6w6s e162wx9x0").text.strip()


        image_path = download_image(image_url, save_brand)

        if brand in car_data_by_brand:
            car_data_by_brand[brand].append({
                "title": save_brand,
                "image_url": image_url,
                "price": price,
                "brend": brand,
                "path_image": image_path,
                "car_info": all_car_info,
            })
        else:
            car_data_by_brand[brand] = [{
                "title": save_brand,
                "image_url": image_url,
                "price": price,
                "brend": brand,
                "path_image": image_path,
                "car_info": all_car_info,
            }]

        json_file_path = f"json_database/{brand}_data.json"
        with open(json_file_path, "w") as json_file:
            json.dump(car_data_by_brand[brand], json_file, indent=4)
