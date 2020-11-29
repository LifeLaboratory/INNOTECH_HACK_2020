import requests as req
import urllib3
import traceback
urllib3.disable_warnings()


class EgrulNalogClient:
    def __init__(self):
        self.session = req.Session()
        self.base_host = 'https://egrul.nalog.ru'

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()

    @staticmethod
    def _write_pdf(pdf, filename):
        try:
            with open(f'app/data/{filename}.pdf', 'wb') as f:
                f.write(pdf)
                return filename
        except Exception:
            traceback.print_exc()
            return


    @staticmethod
    def _parse_get_params(params):
        params_dict = {x[0]: x[1] for x in [x.split("=") for x in params[1:].split("&")]}
        print(params_dict)

    def _get_url(self, endpoint):
        return self.base_host + endpoint

    def _make_request(self, method='GET', endpoint='', headers=None, cookies=None, **kwargs):
        self.session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0)'})
        if headers:
            self.session.headers.update(headers)

        if cookies:
            self.session.cookies.update(cookies)

        kwargs.update({'verify': False})

        response = self.session.request(method, self._get_url(endpoint), **kwargs)
        return response

    def _search_result(self, extract_id):
        response = self._make_request('GET', f'/search-result/{extract_id}').json()
        rows = response.get('rows')
        if not rows:
            return

        return rows[0]

    def _vyp_request(self, token):
        response = self._make_request('GET', f'/vyp-request/{token}').json()
        return response.get('t')

    def _vyp_status(self, token):
        return self._make_request('GET', f'/vyp-status/{token}').json()

    def _vyp_download(self, token):
        return self._make_request('GET', f'/vyp-download/{token}').text.encode()

    def get_inn(self, query: str, nameEq: str) -> int:
        """
            example:
            :param query: Укажите ИНН или ОГРН (ОГРНИП) или наименование ЮЛ, ФИО ИП
            :param nameEq: Принимает "on" или "off"
            :param region: Номер региона "01" или "99" или "01%2c99"
        """
        data = {
            'query': query,
            'nameEq': nameEq,
        }

        info_id = self._search_info(**data)
        if not info_id:
            return

        result = self._search_result(info_id)
        if not result:
            return

        return int(result.get('i'))

    def _search_info(self, **kwargs):
        info = self._make_request('POST', '/', data=kwargs).json()

        if not info:
            print('Не могу получить сведения о компаниях')
            return

        info_id = info.get('t')
        captcha_id = info.get('captchaRequired')

        if 'captchaRequired' in info.keys() and captcha_id:
            print('Нужна капча')
            return

        return info_id


if __name__ == '__main__':
    client = EgrulNalogClient()
    client.get_inn('7713065557', "on")
