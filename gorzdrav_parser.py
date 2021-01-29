import requests
import pprint
import time
from datetime import datetime

def send_push(text):
    try:
        print(f"Send push: {text}")
        TOKEN = "put your token here"
        args = {"title": text, "identifier": TOKEN}
        requests.get("https://pushmeapi.jagcesar.se", params=args)
    except Exception as e:
        print(f"Error send push {e}")


def get_data(district_id):
    data = None
    try:
        
        GET_URL = f"https://gorzdrav.spb.ru/_api/api/district/{district_id}/lpu"
        r = requests.get(GET_URL)
        data = r.json()

        if r.status_code != 200:
            send_push("ERROR get data")
    except Exception as e:
        print(e)
        send_push("ERROR get data")

    return data


send_push("Hello from python")

# Get info from https://gorzdrav.spb.ru/service-covid-vaccination-schedule 
# Put your hospital number here
HOSPITAL_NAME_PATTERN = "78"
# District ID
DISTRIC_ID = 17
REFRESH_PERIOD = 10 * 60
RETRY_PERIOD = 5 * 60

while True:
    print("---------------------------------------------------------")
    now = datetime.now()
    print(now.strftime("%d/%m/%Y %H:%M:%S"))

    data = get_data(DISTRIC_ID)
    if not data:
        send_push(f"No data, wait {RETRY_PERIOD} and try againt")
        time.sleep(REFRESH_PERIOD)
        continue

    try:
        for item in data["result"]:
            if HOSPITAL_NAME_PATTERN in item["lpuShortName"]:
                print(f"Check hospital {item['lpuShortName']}")
                print(item["covidVaccination"])

                if item["covidVaccination"]:
                    send_push("REGISTRATION IS OPEN")
    except Exception as e:
        send_push(f"Error parse responce {e}")

    time.sleep(REFRESH_PERIOD)
