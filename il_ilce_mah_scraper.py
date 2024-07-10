# This script scrapes sahibinden.com for City(il), Town(ilce) and District/Quarter(mah) ids
# The resulting json format is as such:
# {"il": [{"id": city_id, "name": city_name}, ...],
#  "ilce": [{"id": town_id, "name": town_name, "city_id": city_id}, ...], 
#  "mah": [{"id": quarter_id, "name": quarter_name, "city_id": city_id, "town_id": town_id}, ...]
# }
import requests
import json
import time
import warnings

# Suppressing warnings
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made.*")


CITIES_URL = "https://34.120.52.83/ajax/rei/cities"
TOWNS_URL = "https://34.120.52.83/ajax/rei/towns?&cityId="
QUARTERS_URL = "https://34.120.52.83/ajax/rei/quarters?cityId={}&townId={}"

def get_il():
    """Fetches city data."""
    response = requests.get(CITIES_URL, verify=False)
    response.raise_for_status()
    return [{"id": city["id"], "name": city["name"]} for city in response.json()]

def get_ilce(city_id):
    """Fetches town data for a given city."""
    response = requests.get(TOWNS_URL + str(city_id), verify=False)
    response.raise_for_status()
    return [{"id": town["id"], "name": town["name"], "city_id": city_id} for town in response.json()]

def get_mah(city_id, town_id):
    """Fetches quarter data for a given city and town."""
    response = requests.get(QUARTERS_URL.format(city_id, town_id), verify=False)
    response.raise_for_status()
    return [{"id": quarter["id"], "name": quarter["name"], "city_id": city_id, "town_id": town_id} for quarter in response.json()]

def save_to_json(data, filename):
    """Saves data to a JSON file."""
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

if __name__ == "__main__":
    result = {"il": [], "ilce": [], "mah": []}
    ilce_count = 0
    mah_count = 0

    print("---Scrapping Started---")
    print("Srapping Cities")
    il_data = get_il()
    result["il"] = il_data
    il_count = len(il_data)
    print("Cities Finished")
    print("------------------")

    print("Scrapping Towns")
    for city in result["il"]:
        ilce_data = get_ilce(city['id'])
        ilce_count += len(ilce_data)
        result["ilce"].extend(ilce_data)
    print("Towns Finished")
    print("------------------")

    print("Scrapping Quarters")
    for town in result["ilce"]:
        mah_data = get_mah(town['city_id'], town['id'])
        mah_count += len(mah_data)
        result["mah"].extend(mah_data)
    print("Quarters Finished")
    print("------------------")

    filename = f"il_ilce_mah_{int(time.time())}.json"
    save_to_json(result, filename)
    print(f"Saved to {filename}")
    print(f"Counted Cities: {il_count}\nScrapped Cities: {len(result['il'])}\n")
    print(f"Counted Towns: {ilce_count}\nScrapped Towns: {len(result['ilce'])}\n")
    print(f"Counted Quarters: {mah_count}\nScrapped Quarters: {len(result['mah'])}")
