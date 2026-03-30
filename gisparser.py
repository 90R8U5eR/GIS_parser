import requests
from bs4 import BeautifulSoup as bs
import json
from datetime import datetime

def fetch_page(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise an error for bad responses
    return bs(response.text, 'html.parser')

def parse_data(soup, selector, attribute=None, is_text=True):
    data = []
    elements = soup.select(selector)
    for element in elements:
        if attribute:
            value = element.attrs.get(attribute)
        else:
            value = element.text.strip() if is_text else None
        if value:
            data.append(value)
    return data

def main(url):
    soup = fetch_page(url)

    # Parse various weather data
    pogoda_data = {
        'date': str(datetime.now()),
        'time': parse_data(soup, "div.widget-row.widget-row-datetime-time span"),
        'temperature': parse_data(soup, 'div[data-row="temperature-air"] temperature-value', 'value', is_text=False),
        'wind direction': parse_data(soup, 'div[data-row="wind-direction"] div.direction'),
        'windspeed': parse_data(soup, 'div[data-row="wind-gust"] speed-value', 'value', is_text=False),
        'precipitation': parse_data(soup, 'div[data-row="precipitation-bars"] div.item-unit'),
        'pressure': parse_data(soup, 'div[data-row="pressure"] pressure-value', 'value', is_text=False),
        'humidity': parse_data(soup, 'div[data-row="humidity"] div'),
        'icons': parse_data(soup, 'div[data-row="icon-tooltip"] use', 'href', is_text=False)
    }

    print(pogoda_data)
    
    with open('data_pogoda.json', 'w', encoding='utf-8') as f:
        json.dump(pogoda_data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    url = 'https://www.gismeteo.ru/weather-orel-4432/'
    main(url)
