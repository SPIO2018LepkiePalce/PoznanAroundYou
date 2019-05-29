import os
import requests
import json
#added for test

class BikeRackJSON:
    def __init__(self):
        self.bikejson = ""

        if not os.path.isfile('bikes.txt'):
            self.update_bikes_file()
        else:
            self.bikejson = self.read_bikes_file()

    def get_json(self):
        return self.bikejson

    def update_bikes_file(self):
        with open("bikes.txt", "w", encoding="utf-8") as bikefile:
            json.dump(self.download_json_from_api(), bikefile)

    def read_bikes_file(self):
        with open("bikes.txt", "r", encoding="utf-8") as bikefile:
            return json.load(bikefile)

    def download_json_from_api(self):
        url = "http://www.poznan.pl/mim/plan/map_service.html?mtype=pub_transport&co=stacje_rowerowe"
        r = requests.get(url)
        return r.json()


brj = BikeRackJSON()

print(brj.bikejson)

