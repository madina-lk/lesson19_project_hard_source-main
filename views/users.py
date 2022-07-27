from flask_restx import Resource, Namespace
from flask import request

from dao.model.users import UserSchema
from implemented import user_service
from decorators import auth_required, admin_required

user_ns = Namespace('users')


@user_ns.route('/')
class UsersView(Resource):
    # @admin_required
    def get(self):
        users = user_service.get_all()
        responce = UserSchema(many=True).dump(users)

        return responce, 200

    def post(self):
        data = request.json
        user = user_service.create(data)

        return '', 200


