import requests
import unittest
import json

class ServiceAPIJSON:
    def __init__(self, type):
        self.status_code = 0
        self.service_api_json = self.download_json_from_api(type)
        self.save_json_to_file(type)

    def get_json(self):
        return self.service_api_json

    def save_json_to_file(self, type):
        with open(type + "_JSON.txt", "w") as jsonfile:
            json.dump(self.get_json(), jsonfile)

    def download_json_from_api(self, type):
        if type == "STOPS":
            url = "http://www.poznan.pl/mim/plan/map_service.html?mtype=pub_transport&co=cluster"
        elif type == "TICKETMACHINES":
            url = "http://www.poznan.pl/mim/plan/map_service.html?mtype=pub_transport&co=class_objects&class_id=4000"
        elif type == "BIKES":
            url = "http://www.poznan.pl/mim/plan/map_service.html?mtype=pub_transport&co=stacje_rowerowe"
        else:
            return {}

        try:
            r = requests.get(url)
            self.status_code = r.status_code
        except ConnectionError:
            return {}
        self.status_code = r.status_code
        return r.json()



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