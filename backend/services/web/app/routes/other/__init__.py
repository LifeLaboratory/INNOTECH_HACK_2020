from flask_restplus import Resource, reqparse
from app import ns_api
from werkzeug.datastructures import FileStorage
import secrets
from app.utils.sql_function import get_all_client_info


@ns_api.route('/upload_image', methods=['POST'])
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
        answer = get_all_client_info(1)
        #return {'status': 'ok', 'message': "image was uploaded"}
        return answer