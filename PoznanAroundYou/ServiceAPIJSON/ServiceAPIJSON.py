import requests
import unittest
import json
import os
import time
from datetime import datetime

SUFFIX = "_JSON.txt"
LOGFILENAME = "log.txt"

def log_event(txt):
    logstring = " ".join((datetime.utcnow().strftime('%d.%m.%y - %H:%M:%S.%f'), txt, "\n"))

    if os.path.isfile(LOGFILENAME):
        with open(LOGFILENAME, "a") as logfile:
            logfile.write(logstring)
    else:
        with open(LOGFILENAME, "w") as logfile:
            logfile.write(logstring)


class ServiceAPIJSON:
    def __init__(self, type):
        self.type = type
        self.status_code = 0
        self.service_api_json = ""
        self.load_json_from_either_api_or_file()

    def get_file_age(self):
        if os.path.isfile(self.type + SUFFIX):
            return int(time.time() - os.path.getmtime(self.type + SUFFIX))
        else:
            return 9999

    def get_json(self):
        return self.service_api_json

    def save_json_to_file(self):
        with open(self.type + SUFFIX, "w") as jsonfile:
            json.dump(self.get_json(), jsonfile)
        log_event(self.type + " was saved to file")

    def read_json_from_file(self):
        with open(self.type + SUFFIX, "r") as jsonfile:
            self.service_api_json = json.load(jsonfile)
        log_event(self.type + " was read from file")

    def download_json_from_api(self):
        if self.type == "STOPS":
            url = "http://www.poznan.pl/mim/plan/map_service.html?mtype=pub_transport&co=cluster"
        elif self.type == "TICKETMACHINES":
            url = "http://www.poznan.pl/mim/plan/map_service.html?mtype=pub_transport&co=class_objects&class_id=4000"
        elif self.type == "BIKES":
            url = "http://www.poznan.pl/mim/plan/map_service.html?mtype=pub_transport&co=stacje_rowerowe"
        else:
            return {}

        try:
            r = requests.get(url)
            self.status_code = r.status_code
        except ConnectionError:
            return {}
        self.status_code = r.status_code
        self.service_api_json = r.json()
        log_event(self.type + " was read from online API")

    def load_json_from_either_api_or_file(self):
        log_event(self.type + " request logged, the file is " + str(self.get_file_age()) + " seconds old")
        if self.get_file_age() < 300:
            self.read_json_from_file()
        else:
            self.download_json_from_api()
            self.save_json_to_file()


class TestServiceAPIJSON(unittest.TestCase):
    def test_no_type(self):
        service = ServiceAPIJSON("")
        self.assertEqual(service.get_json(), {})

    def test_correct_type(self):
        service = ServiceAPIJSON("STOPS")
        self.assertNotEqual(service.get_json(), {})

    def test_if_json_data_returned_for_bikes(self):
        service = ServiceAPIJSON("BIKES")
        thing = service.get_json()
        self.assertTrue("features" in thing.keys())

    def test_if_json_data_returned_for_ticketmachines(self):
        service = ServiceAPIJSON("TICKETMACHINES")
        thing = service.get_json()
        self.assertTrue("features" in thing.keys())

    def test_if_json_data_returned_for_stops(self):
        service = ServiceAPIJSON("STOPS")
        thing = service.get_json()
        self.assertTrue("features" in thing.keys())


if __name__ == '__main__':
    unittest.main()
    # saj = ServiceAPIJSON("BIKES")
    # print(saj.get_json())