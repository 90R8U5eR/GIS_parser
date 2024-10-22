import requests
from bs4 import BeautifulSoup as bs
import json
from datetime import datetime

def pogoda(url):
    response = requests.get(url, headers={
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 "
                      "Safari/537.36"})
    soup = bs(response.text, 'html.parser')

    # Парсим время
    # Ищем тег span с родительским тегом div с классами widget-row и widget-row-datetime-time
    time_data=[]
    times = soup.select("div.widget-row.widget-row-datetime-time span")
    for time in times:
      time_data.append(time.text.strip())
    print(time_data)

    # Парсим температуру в градусах
    # Ищем тег temperature-value с родительским тегом div с data-row="temperature-air"
    # Потом достаем температуру из аттрибута value
    temp_data=[]
    temps = soup.select('div[data-row="temperature-air"] temperature-value[from-unit="c"] ')
    for temp in temps:
      temp_data.append(temp.attrs["value"])
    print(temp_data)

    # Парсим порывы ветра м/с
    # Ищем тег speed-value с родительским тегом div с data-row="temperature-air"
    wind_gust_data=[]
    wind_gusts = soup.select('div[data-row="wind-gust"] speed-value[from-unit="ms"]')
    for wind_gust in wind_gusts:
      wind_gust_data.append(wind_gust.attrs["value"])
    print(wind_gust_data)

    # Парсим направление ветра
    # Ищем тег div класса direction с родительским тегом div с data-row="wind-direction"
    # Потом достаем температуру из аттрибута value
    wind_direction_data=[]
    wind_directions = soup.select('div[data-row="wind-direction"] div.direction')
    for wind_direction in wind_directions:
      wind_direction_data.append(wind_direction.text.strip())
    print(wind_direction_data)

    # Парсим осадки в мм
    # Ищем тег div класса item-unit с родительским тегом div с data-row="precipitation-bars"
    # Потом достаем температуру из аттрибута value
    precipitation_data=[]
    precipitations = soup.select('div[data-row="precipitation-bars"] div.item-unit')
    for precipitation in precipitations:
      precipitation_data.append(precipitation.text.strip())
    print(precipitation_data)

    # Парсим давление в мм.рт.ст.
    # Ищем тег pressure-value с родительским тегом div с data-row="pressure"
    # Потом достаем температуру из аттрибута value
    pressure_data=[]
    pressures = soup.select('div[data-row="pressure"] pressure-value[from-unit="mmhg"] ')
    for pressure in pressures:
      pressure_data.append(pressure.attrs["value"])
    print(pressure_data)

    # Парсим влажность в %
    # Ищем тег div с родительским тегом div с data-row="humidity"
    # Потом достаем температуру из аттрибута value
    humidity_data=[]
    humiditys = soup.select('div[data-row="humidity"] div')
    for humidity in humiditys:
      humidity_data.append(humidity.text.strip())
    print(humidity_data)

    # Парсим иконки
    # Ищем тег use с родительским тегом div с data-row="icon-tooltip"
    # Потом достаем температуру из аттрибута value
    icon_data=[]
    icons = soup.select('div[data-row="icon-tooltip"] use[href]')
    for icon in icons:
      icon_data.append(icon.attrs["href"])
    print(icon_data)


    #with open('pogoda.html', 'w', encoding='utf-8') as f:
    #    f.write(str(soup))

    pogoda_data = {'date': str(datetime.now()), 'time':time_data, 'temperature': temp_data, 'wind direction': wind_direction_data, 'windspeed': wind_gust_data, 'precipitation': precipitation_data, 'pressure': pressure_data, 'humidity': humidity_data, 'icons': icon_data}
    print(pogoda_data)
    with open('data_pogoda.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(pogoda_data, ensure_ascii=False, indent=4))



if __name__ == "__main__":
  url = 'https://www.gismeteo.ru/weather-orel-4432/'
  pogoda(url)
