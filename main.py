import requests

TFL_API_BASE_URL = "https://api.tfl.gov.uk"


def find_station_id(station_name):
    url = TFL_API_BASE_URL + f"/StopPoint/Search?query={station_name}&modes=tube"
    response = requests.get(url)

    if response.status_code == 200:
        search_results = response.json()["matches"]
        for result in search_results:
            if result["name"].lower() == station_name.lower():
                return result["id"]
    else:
        print(f"Error: {response.status_code}")
        return None


def find_crowd_levels(station_id):
    url = TFL_API_BASE_URL + f"/crowding/{station_id}/Live"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()["percentageOfBaseline"]
    else:
        print(f"Error: {response.status_code}")
        return None

def find_line_id(line_name):
    url = TFL_API_BASE_URL + f"/Line/Mode/tube"
    response = requests.get(url)
    if response.status_code == 200:
        lines = response.json()
        for line in lines:
            if line["name"].lower() == line_name.lower():
                return line["id"]
    else:
        print(f"Error: {response.status_code}")
        return None

def find_arrivals(station_id):
    url = TFL_API_BASE_URL + f"/StopPoint/{station_id}/Arrivals"
    response = requests.get(url)
    if response.status_code == 200:
        arrivals = response.json()
        return arrivals
    else:
        print(f"Error: {response.status_code}")
        return None


if __name__ == "__main__":
    station_name = "Fulham Broadway Underground Station"
    station_id = find_station_id(station_name)
    # line_name = "District"
    # line_id = find_line_id(line_name)
    if station_id:
        print(f"The station ID for {station_name} is {station_id}.")
        if crowd_levels := find_crowd_levels(station_id):
            print(f"The current crowd levels are {crowd_levels}% of baseline.")
        else:
            print(f"Error: Could not find crowd levels for {station_name}.")
        if arrivals := find_arrivals(station_id):
            print(f"The next 2 arrivals are:")
            for arrival in arrivals[:2]:
                print(f"{arrival['platformName']} -> {arrival['destinationName']} @ {arrival['expectedArrival']} ({arrival['timeToStation']} seconds)")
        # if line_id:
        #     print(f"The line ID for {line_name} is {line_id}.")
        # else:
        #     print(f"Line ID not found for {line_name}.")
    else:
        print(f"Station ID not found for {station_name}.")
