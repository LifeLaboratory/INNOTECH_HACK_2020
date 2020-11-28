from app import ns_api
from flask_restplus import fields

egrul_info_request = ns_api.model('EgrulInfo', {
    'query': fields.String('Иван'),
    'nameEq': fields.String('on'),
    'region': fields.String('03,02,99')
})
