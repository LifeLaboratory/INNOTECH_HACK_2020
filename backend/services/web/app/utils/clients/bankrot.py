import requests as req
import urllib3

urllib3.disable_warnings()


class BankrotClient:
    def __init__(self):
        self.session = req.Session()
        self.base_host = 'https://egrul.nalog.ru'




if __name__ == '__main__':
    client = EgrulNalogClient()
    client.download('31747040005155', [78], True)

