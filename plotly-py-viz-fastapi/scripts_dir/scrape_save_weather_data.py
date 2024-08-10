import requests
import pandas as pd
from bs4 import BeautifulSoup
from io import StringIO
import json

save_path = "../datasets/weather_data.csv"

# Import city codes from JSON file
with open("../datasets/jsons/city_codes_en.json", "r") as f:
    city_codes = json.load(f)
    cities = [
        city.upper() for city in city_codes.keys()
    ]  # Convert city names to uppercase for consistency with the URL structure
    cities.remove("mersin".upper())


with open("../datasets/jsons/city_codes_tr.json", "r") as f:
    city_codes = json.load(f)
    cities_tr = [
        city for city in city_codes.keys()
    ]  # Convert city names to uppercase for consistency with the URL structure
    cities_tr.remove("İçel")


def export_to_csv(save_path, df):
    df.to_csv(save_path, index=False)


def scrape_city_data(city, city_code):
    global cities_tr
    url = f"https://www.mgm.gov.tr/veridegerlendirme/il-ve-ilceler-istatistik.aspx?m={city}"
    response = requests.get(url)
    response.raise_for_status()  # Ensure the request was successful

    soup = BeautifulSoup(response.content, "html.parser")

    # Find all tables on the page
    tables = soup.find_all("table")

    if not tables:
        print(f"No tables found for city: {city}")
        return None

    # Get the HTML string of the first table
    table_html = str(tables[0])

    # Replace commas with dots for proper decimal representation
    table_html = table_html.replace(",", ".")
    # Wrap the HTML string in a StringIO object
    table_io = StringIO(table_html)

    # Parse the first table into a pandas dataframe
    df = pd.read_html(table_io, header=0)[0]
    df.drop(columns=["Yıllık"], inplace=True)  # Remove unnecessary column
    # Remove first, eighth and eleventh row,
    df.drop(df.index[[0, 7, 10]], inplace=True)
    # Rename the columns, except the first column, to 1-12
    df_col = ["0"]
    df_col.extend([f"{i+1}" for i in range(len(df.columns) - 1)])
    df.columns = df_col
    # Change the type of columns to numeric type, except the first column
    df.iloc[:, 1:] = df.iloc[:, 1:].astype(float)
    # Create a column and insert it at first position. This column will hold the city code
    df.insert(0, "il", cities_tr[city_code - 1])
    df.insert(0, "il kodu", city_code)

    return df


def scrape_and_save_weather_data():

    not_found_cities = []
    city_data_list = []
    # Example usage
    for city_code, city in enumerate(cities):
        city = (
            city.upper()
        )  # Convert city name to uppercase for consistency with the URL structure
        city_data = scrape_city_data(city, city_code + 1)
        if city_data is not None:
            city_data_list.append(city_data)
        else:
            print(f"NO DATA FOUND FOR: {city}")
            not_found_cities.append(city)

    concatenated_df = pd.concat(city_data_list, ignore_index=True)
    export_to_csv(save_path, concatenated_df)
