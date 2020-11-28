from flask_restplus import Resource, reqparse
from app.routes.egrul_nalog.provider import Provider
from app.routes.egrul_nalog.models import *
from app import ns_api
from app.utils.clients.egrul_nalog import EgrulNalogClient

"""
model = api.model('Class', {'status': fields.String('Ok')})
Мы говорим, что работаем со словарём, в нём будет ключ 'status', а значение должно быть string. По дефолту "Ok"

@ns_api.response(404, 'User not found') - В документации покажем, что на 404 HTTP статус код - это 'User not found'
@ns_api.expect(model) - пример json'а, который мы ожидаем от клиента
@ns_api.marshal_with(model) - Пример json'а, который пользователь на определённый HTTP код. 200 по дефолту.
@ns_api.route('/path_to') - куда нужно обратиться для выполнения метода. https://example.com/api/path_to

abort(404) - вернуть ошибку 404.
api.payload - прочитать json из запроса. Работает только для POST.
"""

'''
Сделать парсер аргументов
Писать логи body в access.log
'''


@ns_api.route('/get_egrul_info')
class Users(Resource):
    # @ns_api.marshal_with(egrul_info_response)
    @ns_api.expect(egrul_info_request)
    def get(self):
        """Предоставление сведений из ЕГРЮЛ/ЕГРИП"""
        parser = reqparse.RequestParser()
        parser.add_argument('query', help='Укажите ИНН или ОГРН (ОГРНИП) или наименование ЮЛ, ФИО ИП')
        parser.add_argument('name', help='Искать по точному соответствию наименования юридического лица или фамилии, имени и отчеству')
        parser.add_argument('region', help='Выбрать регионы(список)')

        return {'status': 'ok'}
