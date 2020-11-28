from flask_restplus import Resource, reqparse

from app.config import VK_LOGIN, VK_PASSWORD
from app.routes.egrul_nalog.provider import Provider
from app.routes.egrul_nalog.models import *
from app import ns_api
from app.utils.clients.egrul_nalog import EgrulNalogClient
import vk_api

vk_session = vk_api.VkApi(VK_LOGIN, VK_PASSWORD)
vk_session.auth()

vk = vk_session.get_api()


@ns_api.route('/social/user/<int:user_id>', methods=['GET'])
class Social(Resource):
    def get(self, user_id):
        return {
            'ID': user_id,
            'USER': vk.users.get(user_ids=str(user_id), fields='photo_max,sex,bdate,contacts,site,photo_max_orig')
        }
