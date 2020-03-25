import requests
import json


# Fetches new data and overwrite the local data

def update_data():

    url = "https://pomber.github.io/covid19/timeseries.json"
    r = requests.get(url)
    data = r.json()
    print("Lastest Data: " + data["United Kingdom"][-1]["date"])
    with open('data.json', 'w') as f:
        json.dump(data, f)


if __name__ == '__main__':
    update_data()