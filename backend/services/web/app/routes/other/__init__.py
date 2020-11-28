from flask_restplus import Resource, reqparse
from app.routes.egrul_nalog.provider import Provider
from app.routes.egrul_nalog.models import *
from app import ns_api
from werkzeug.datastructures import FileStorage
import secrets


@ns_api.route('/upload_image')
class Image(Resource):
    def post(self):
        """Предоставление сведений из ЕГРЮЛ/ЕГРИП"""
        parser = reqparse.RequestParser()
        parser.add_argument('image', type=FileStorage, location='files', required=True)
        args = parser.parse_args()

        if not args.get('image'):
            return {'status': 'No image field'}, 400

        extension = args.get('image').mimetype.split('/')[-1]
        if extension not in ('png', 'jpg', 'jpeg'):
            return {'status': 'Missing mimetype'}, 400
        
        args.get('image').save(f'/web/app/static/{secrets.token_hex(15)}.{extension}')

        return {'status': 'ok', 'message': "image was uploaded"}