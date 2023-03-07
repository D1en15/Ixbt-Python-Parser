import requests
from bs4 import BeautifulSoup
import lxml
import json
from datetime import date
import time

def today_news_update():
    date_today = str(date.today()).replace('-', '/')

    url = f"https://www.ixbt.com/news/{date_today}"
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"}
    r = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')
    all_news = soup.find_all('li', class_='item')

    while True:
        ixbt_dict = {}
        for items in all_news:
            item_time = items.find('span', class_='time_iteration_icon').text.strip()
            item_title = items.find('strong').text.strip()
            item_url = f"https://www.ixbt.com{items.find('a', href=True)['href'].split('#')[0]}"

            item_id = item_url.split('/')[-1][:-5]

            ixbt_dict[f"{date_today}|{item_id}"] = {
                'item_time': item_time,
                'item_title': item_title,
                'item_url': item_url
            }

        with open('ixbt_dict.json', 'w', encoding='utf-8') as file:
            json.dump(ixbt_dict, file, indent=4, ensure_ascii=False)
        time.sleep(10)


def main():
    today_news_update()

if __name__=="__main__":
    main()