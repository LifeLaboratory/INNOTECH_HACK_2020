from flask_restplus import Resource
from app import ns_api
from app.config import REPO_NAME
import os
import socket
import json

@ns_api.route('/git.webhook', methods=['POST'])
class GitWebhook(Resource):

    def post(self):
        if not ns_api.payload:
            return {'status': 'error'}, 403
            
        repo = ns_api.payload.get('repository')
        
        if not repo or repo.get('name') != REPO_NAME:
            return {'status': 'error'}, 403
                        
        SOCKET_FILE = '/tmp/sockets/git-webhook.sock'

        if not os.path.exists(SOCKET_FILE):
            return {'status': 'error'}, 500

        with socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM) as client:
            client.connect(SOCKET_FILE)
            client.sendall(bytearray('\xDE\xAD\xBE\xEF', 'utf-8'))

        return {'status': 'ok'}
