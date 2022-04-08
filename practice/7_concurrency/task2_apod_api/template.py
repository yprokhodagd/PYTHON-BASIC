import json
import multiprocessing
from datetime import timedelta, datetime
from pathlib import Path
from multiprocessing import Pool
import requests as requests

API_KEY = "LnRSSryolbcE54eb4gXoaYxgeJAvzl9Pp49TyQQa"
APOD_ENDPOINT = 'https://api.nasa.gov/planetary/apod'
OUTPUT_IMAGES = './output'


def get_apod_metadata(start_date: str, end_date: str, api_key: str) -> list:
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    delta = end_date - start_date
    urls = []
    for i in range(delta.days + 1):
        day = start_date + timedelta(days=i)
        day_str = str(day).split(" ")[0]

        response = requests.get(f"https://api.nasa.gov/planetary/apod?api_key={api_key}&date={day_str}")

        url = json.loads(response.text)['url']
        urls.append(url)

    return urls


def download_apod_image(url):
    name = url.split('/')[-1]
    img_data = requests.get(url).content
    path = Path("Image_folder", name)
    with open(path, 'wb') as handler:
        handler.write(img_data)


def main():
    urls_list = get_apod_metadata(
        start_date='2021-08-01',
        end_date='2021-08-10',
        api_key=API_KEY,
    )

    pool = Pool()
    pool.map(download_apod_image, urls_list)


if __name__ == '__main__':
    main()
