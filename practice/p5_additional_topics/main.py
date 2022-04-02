import json
import os
from pathlib import Path
import xml.etree.cElementTree as ET

SOURCE_PATH = "/Users/yprokhoda/repo/PYTHON-BASIC/practice/p5_additional_topics/parsing_serialization_task/source_data/"
all_cities = []


def find_numbers(values):
    min_ = min(values)
    max_ = max(values)
    mean_ = round(sum(values) / len(values), 2)
    return min_, max_, mean_


def get_data():
    all_folders = [x[0] for x in os.walk(SOURCE_PATH)]
    for city_folder in all_folders[1:]:  # first 2 are no city folders
        city_name = city_folder.split('/')[-1]
        city_json_file = Path(city_folder, "2021_09_25.json")
        with open(city_json_file, "r") as f:
            city_data = json.load(f)
            temp_values = []
            wind_values = []
            for hour in city_data['hourly']:
                temp_values.append(hour['temp'])
                wind_values.append(hour['wind_speed'])

            # Calculate mean, maximum, minimum temperature
            min_temp, max_temp, mean_temp = find_numbers(temp_values)

            # Calculate mean, maximum, minimum wind speed
            min_wind, max_wind, mean_wind = find_numbers(wind_values)

            city = {"city": city_name, "min_temp": min_temp, "max_temp": max_temp, "mean_temp": mean_temp,
                    "min_wind_speed": min_wind, "max_wind_speed": max_wind, "mean_wind_speed": mean_wind}

        all_cities.append(city)
    print(all_cities)
    # Calculate mean temperature and wind speed for the whole country by using produced data before.
    mean_temperature_country = round(sum([i['mean_temp'] for i in all_cities]) / len(all_cities), 2)
    mean_wind_speed_country = round(sum([i['mean_wind_speed'] for i in all_cities]) / len(all_cities), 2)
    print("mean_temperature_country", round(mean_temperature_country, 2))
    print("mean_wind_speed_country", round(mean_wind_speed_country, 2))
    # Find the coldest, the warmest and the windiest cities in Spain (you must use mean values from step 2 to do that).
    coldest_city = min(all_cities, key=lambda x: x['mean_temp'])['city']
    warmest_city = max(all_cities, key=lambda x: x['mean_temp'])['city']
    windiest_city = max(all_cities, key=lambda x: x['max_wind_speed'])['city']
    print("coldest_city", coldest_city)
    print("warmest_city", warmest_city)
    print("windiest_city", windiest_city)

    # get_data()

    weather = ET.Element("weather",country="Spane", date="2021-09-25")
    summary = ET.SubElement(
        weather, "summary",
        mean_temp=str(mean_temperature_country),
        mean_wind_speed=str(mean_wind_speed_country),
        coldest_place=coldest_city,
        warmest_place=warmest_city,
        windiest_place=windiest_city,
    )
    cities = ET.SubElement(weather, "cities")
    for city in all_cities:
        ET.SubElement(cities, city["city"].replace(" ", "_"),
                      min_temp=str(city["min_temp"]), max_temp=str(city["max_temp"]), mean_temp=str(city["mean_temp"]),
                      min_wind_speed=str(city["min_wind_speed"]), max_wind_speed=str(city["max_wind_speed"]), mean_wind_speed=str(city["mean_wind_speed"]))


    tree = ET.ElementTree(weather)
    ET.indent(tree, space="\t", level=0)
    tree.write("filename.xml", encoding="utf-8")


if __name__ == "__main__":
    get_data()
