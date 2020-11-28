from app import ns_api
from flask_restplus import fields

user = ns_api.model('CreateUser', {
    'username': fields.String('madwayz'),
    'firstname': fields.String('Роман'),
    'surname': fields.String('Николенко')
})

user_data = ns_api.inherit('GetUser', user, {
    'ID': fields.Integer('1')
})

user_created = ns_api.model('UserCreated', {'message': fields.String('User is created')})
user_updated = ns_api.model('UserUpdated', {'message': fields.String('User has been updated')})
user_deleted = ns_api.model('UserDeleted', {'message': fields.String('User has been deleted')})
