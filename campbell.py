import requests

class campbell():
    def __init__(self, address) -> None:
        self.address = address

    def print_latest_data(self, table) -> None:
        command = "dataquery"
        format = "json"
        mode = "backfill"
        parameter = "p1=1"

        url = f"http://{self.address}/?command={command}&uri=dl:{table}&format={format}&mode={mode}&{parameter}"

        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            date, time = data["data"][0]["time"].split("T")
            print(f"Date:\t\t{date}")
            print(f"Time:\t\t{time}\tUTC")
            for i in range(len(data["head"]["fields"])):
                field = data["head"]["fields"][i]['name']
                value = data["data"][1]["vals"][i]

                try: 
                    units = data["head"]["fields"][i]["units"]
                except KeyError:
                    units = ""

                if len(field) > 7:
                    print(f"{field}\t{value}\t\t{units}")
                else:
                    print(f"{field}\t\t{value}\t\t{units}")
        else:
            print(f"Failed to retrieve data: {response.status_code}")