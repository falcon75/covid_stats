import requests
import json


# Fetches new data and overwrite the local data

def update_data():

    url = "https://pomber.github.io/covid19/timeseries.json"
    r = requests.get(url)
    data = r.json()

    with open('data.json', 'r') as f:
        m = f.read()
        m = json.loads(m)

    l_v = m["United Kingdom"][-1]["confirmed"]

    with open('data.json', 'w') as f:
        json.dump(data, f)

    if l_v != data["United Kingdom"][-1]["confirmed"]:
        print("New cases recorded.")
    else:
        print("No new cases.")

    print("Lastest Data: " + data["United Kingdom"][-1]["date"])


if __name__ == '__main__':
    update_data()