from flask_restplus import Resource, reqparse

from app.config import VK_LOGIN, VK_PASSWORD
from app import ns_api
import vk_api
import re
from werkzeug.datastructures import FileStorage
import secrets
import os
import glob
import face_recognition
import numpy as np
import cv2

vk_session = vk_api.VkApi(VK_LOGIN, VK_PASSWORD)
vk_session.auth()

vk = vk_session.get_api()

file_list = glob.glob("app/static/photos/*.jpg")

known_face_encodings = []
known_face_names = []

for photo in file_list:
    known_face_encodings.append(face_recognition.face_encodings(face_recognition.load_image_file(photo))[0])
    known_face_names.append(photo.split(".")[0].split("/")[-1])
print("Пользователи в базе лиц: " + str(known_face_names))


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
            'USER': vk.users.get(user_ids=str(user_id), fields='photo_max,sex,bdate,contacts,site,photo_max_orig')[0],
            'INTERESTS': interests[:10]
        }


@ns_api.route('/social/detect', methods=['POST'])
class Social(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('image', type=FileStorage, location='files', required=True)
        args = parser.parse_args()
        print(args)

        if not args.get('image'):
            return {'status': 'No image field'}, 400

        extension = args.get('image').mimetype.split('/')[-1]
        if extension not in ('png', 'jpg', 'jpeg'):
            return {'status': 'Missing mimetype'}, 400

        path = f'app/static/photos/{secrets.token_hex(15)}.{extension}'
        args.get('image').save(path)

        frame = cv2.imread(path)
        rgb_small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)[:, :, ::-1]
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "UNKNOWN"
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            if face_distances.size > 0:
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]
            face_names.append(name)

        os.remove(path)

        return {
            'USERS': face_names
        }

