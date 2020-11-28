import requests as req
import urllib3
# from bs4 import


urllib3.disable_warnings()


class ArbitrageClient:
    def __init__(self):
        self.session = req.Session()
        self.base_host = 'https://kad.arbitr.ru'

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()

    @staticmethod
    def _parse_get_params(params):
        params_dict = {x[0]: x[1] for x in [x.split("=") for x in params[1:].split("&")]}
        print(params_dict)

    def _get_url(self, endpoint):
        return self.base_host + endpoint

    def _get_courts(self):
        response = self._make_request('POST', '/Kad/SearchInstances', json={})
        print(response.text)

    def _make_request(self, method='GET', endpoint='', headers=None, cookies=None, **kwargs):
        self.session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0)'})
        if headers:
            self.session.headers.update(headers)

        if cookies:
            self.session.cookies.update(cookies)

        kwargs.update({'verify': False})

        response = self.session.request(method, self._get_url(endpoint), **kwargs)
        return response

    def search_instances(self):
        data = {
            "Page": 1,
            "Count": 25,
            "Courts": self._get_courts(),
            "DateFrom": "2020-11-10T00:00:00",
            "DateTo": "2020-11-06T23:59:59",
            "Sides": [
                {"Name": "773370633582", "Type": -1, "ExactMatch": False}
            ],
            "Judges": [
                {"JudgeId": "*", "Type": -1}
            ],
            "CaseNumbers": ["НОМЕР_ДЕЛА"],
            "WithVKSInstances": False
        }
        headers = {'x-data-format': 'iso'}
        response = self._make_request('POST', '/Kad/SearchInstances', headers=headers, json=data)
        print(response)


if __name__ == '__main__':

    client = ArbitrageClient()
    client.search_instances()
