from flask_restplus import Resource, reqparse

from app.config import VK_LOGIN, VK_PASSWORD
from app import ns_api
import vk_api
import re

vk_session = vk_api.VkApi(VK_LOGIN, VK_PASSWORD)
vk_session.auth()

vk = vk_session.get_api()


@ns_api.route('/social/user/<int:user_id>', methods=['GET'])
class Social(Resource):
    def get(self, user_id):
        groups = vk.groups.get(user_id=str(user_id), extended=1)
        words = {}
        for obj in groups['items']:
            for word in obj['name'].split(' '):
                if word == '|' or len(word) < 4 or re.match(r'(^[а-яА-Я]+(ый|ые)$|[0-9]+)', word) is not None or word == 'сообщество' or word == 'Сообщество':
                    continue
                if words.get(word) is None:
                    words[word] = 0
                words[word] = words.get(word) + 1

        interests = [X for X, Y in sorted(words.items(), key=lambda x: x[1], reverse=True)]

        return {
            'ID': user_id,
            'USER': vk.users.get(user_ids=str(user_id), fields='photo_max,sex,bdate,contacts,site,photo_max_orig'),
            'INTERESTS': interests[:10]
        }
