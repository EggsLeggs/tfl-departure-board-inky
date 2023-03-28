import requests

TFL_API_BASE_URL = "https://api.tfl.gov.uk"
STOPPOINT_SEARCH_ENDPOINT = "/StopPoint/Search?query={query}&modes=tube"


def find_station_id(station_name):
    url = TFL_API_BASE_URL + STOPPOINT_SEARCH_ENDPOINT.format(query=station_name)
    response = requests.get(url)

    if response.status_code == 200:
        search_results = response.json()["matches"]
        for result in search_results:
            if result["name"].lower() == station_name.lower():
                return result["id"]
    else:
        print(f"Error: {response.status_code}")
        return None

if __name__ == "__main__":
    station_name = "Fulham Broadway Underground Station"
    station_id = find_station_id(station_name)
    if station_id:
        print(f"The station ID for {station_name} is {station_id}.")
    else:
        print(f"Station ID not found for {station_name}.")
