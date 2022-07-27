import calendar
import datetime

import jwt
from flask import abort

from service.user import UserService

from constants import JWT_SECRET, JWT_ALGORITHMS


class AuthService:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def generate_tokens(self, username, password, is_refresh=False):
        user = self.user_service.get_by_username(username)

        if user is None:
            raise abort(404)

        if not is_refresh:
            if not self.user_service.compare_passwords(user.password, password):
                abort(400)

        data = {
            'username': user.username,
            'role': user.role
        }

        min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        data['exp'] = calendar.timegm(min30.timetuple())
        access_token = jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGORITHMS)

        day130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
        data['exp'] = calendar.timegm(day130.timetuple())
        refresh_token = jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGORITHMS)

        return {
            'access_tocen': access_token,
            'refresh_token': refresh_token
        }

    def approve_refresh_token(self, refresh_token):
        data = jwt.decode(jwt=refresh_token, key=JWT_SECRET, algorithms=[JWT_ALGORITHMS])
        username = data.get('username')

        user = self.user_service.get_by_username(username)
        if not user:
            return False
        now = calendar.timegm(datetime.datetime.utcnow().timetuple())
        expired = data['exp']
        if now>expired:
            return False

        return self.generate_tokens(username, user.password, is_refresh=True)


