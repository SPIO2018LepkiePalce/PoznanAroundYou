import requests

class ServiceAPIJSON:
    def __init__(self, type):
        self.service_api_json = self.download_json_from_api(type)


    def get_json(self):
        return self.service_api_json

    def download_json_from_api(self, type):
        if type == "STOPS":
            url = "http://www.poznan.pl/mim/plan/map_service.html?mtype=pub_transport&co=cluster"
        r = requests.get(url)
        return r.json()