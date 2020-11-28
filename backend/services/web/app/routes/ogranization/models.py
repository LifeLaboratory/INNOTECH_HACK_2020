from app import ns_api
from flask_restplus import fields

vk_link_request = ns_api.model('OgranizationAdd', {
    'vk_link': fields.String('https://vk.com/')
})
