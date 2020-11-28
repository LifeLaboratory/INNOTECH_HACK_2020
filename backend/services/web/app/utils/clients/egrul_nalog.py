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

    def download(self, **kwargs):
        """
        vyp-request
        vyp-status
        vyp-download
        """

        info_id = self._search_info(**kwargs)
        if not info_id:
            return

        result = self._search_result(info_id)

        if not result:
            return

        company_token = result.get('t')
        ogrn = result.get('o')
        inn = result.get('i')

        token = self._vyp_request(company_token)
        response = self._vyp_status(token)

        if response.get('status') != 'ready':
            return

        file = self._vyp_download(token)
        filename = f'{ogrn}_{inn}'
        return self._write_pdf(file, filename)

    def _search_info(self, **kwargs):
        # full_eq = 'on' if full_eq else 'off'
        # regions = '%2c'.join([str(x) if len(str(x)) == 2 else '0' + str(x) for x in regions])
        # data = {
        #     'query': query,
        #     'nameEq': full_eq,
        #     'region': regions,
        # }

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
    # client = EgrulNalogClient()
    # client.download('31747040005155', [78], True)
    a = '{"suggestions":[{"data":{"uri":"773370633582-varlamov-0362","state":{"status":"ACTIVE","code":null,"actuality_date":1577836800000,"registration_date":1360886400000,"liquidation_date":null},"inn":"773370633582","ogrn":"313774604600362","name":{"full_with_opf":"\u0418\u043d\u0434\u0438\u0432\u0438\u0434\u0443\u0430\u043b\u044c\u043d\u044b\u0439 \u043f\u0440\u0435\u0434\u043f\u0440\u0438\u043d\u0438\u043c\u0430\u0442\u0435\u043b\u044c \u0412\u0430\u0440\u043b\u0430\u043c\u043e\u0432 \u0418\u043b\u044c\u044f \u0410\u043b\u0435\u043a\u0441\u0430\u043d\u0434\u0440\u043e\u0432\u0438\u0447","short_with_opf":"\u0418\u041f \u0412\u0430\u0440\u043b\u0430\u043c\u043e\u0432 \u0418\u043b\u044c\u044f \u0410\u043b\u0435\u043a\u0441\u0430\u043d\u0434\u0440\u043e\u0432\u0438\u0447","latin":null,"full":"\u0412\u0430\u0440\u043b\u0430\u043c\u043e\u0432 \u0418\u043b\u044c\u044f \u0410\u043b\u0435\u043a\u0441\u0430\u043d\u0434\u0440\u043e\u0432\u0438\u0447","short":null},"address":{"value":"\u0433 \u041c\u043e\u0441\u043a\u0432\u0430","data":{"region_with_type":"\u0433 \u041c\u043e\u0441\u043a\u0432\u0430"}}}}]}'
    import json
    print(json.loads(a))
