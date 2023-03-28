import requests
from datetime import datetime, timezone
# from inky import InkyPHAT
from PIL import Image, ImageFont, ImageDraw

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


def display_on_inkyphat(text):
    inky_display = InkyPHAT("black")
    inky_display.set_border(inky_display.BLACK)

    img = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(inky_display.FONT, 14)

    draw.text((0, 0), text, inky_display.BLACK, font)
    inky_display.set_image(img)
    inky_display.show()


if __name__ == "__main__":
    station_name = "Fulham Broadway Underground Station"
    station_id = find_station_id(station_name)
    if station_id:
        print(f"The station ID for {station_name} is {station_id}.")
        if crowd_levels := find_crowd_levels(station_id):
            print(f"The current crowd levels are {crowd_levels}% of baseline.")
        else:
            print(f"Error: Could not find crowd levels for {station_name}.")
        if arrivals := find_arrivals(station_id):
            arrivals_text = f"The next 2 arrivals are:\n"
            for arrival in arrivals[:2]:
                arrival_time = datetime.fromisoformat(arrival['expectedArrival'][:-1]).replace(tzinfo=timezone.utc)
                local_arrival_time = arrival_time.astimezone()
                formatted_time = local_arrival_time.strftime('%H:%M:%S')
                arrivals_text += f"{arrival['platformName']} -> {arrival['destinationName']} @ {formatted_time} ({arrival['timeToStation']} seconds)\n"
            print(arrivals_text)
            display_on_inkyphat(arrivals_text)
        else:
            print(f"Error: Could not find arrivals for {station_name}.")
    else:
        print(f"Station ID not found for {station_name}.")
