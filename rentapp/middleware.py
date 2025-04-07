from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from rentapp import settings

import requests
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings


import requests
import jwt
from django.utils.deprecation import MiddlewareMixin


class AutoRefreshJWTMiddleware(MiddlewareMixin):
    def process_request(self, request):
        access_token = request.COOKIES.get("access_token")
        refresh_token = request.COOKIES.get("refresh_token")

        if not self.is_token_expired(access_token=access_token): ### Если токен жив, то вернется None
            request.META["HTTP_AUTHORIZATION"] = f"Bearer {access_token}"
            return None

        if not self.is_token_expired(refresh_token=refresh_token):
            new_access_token = self.refresh_access_token(refresh_token)
            if new_access_token:
                request.META["HTTP_AUTHORIZATION"] = f"Bearer {new_access_token}"
                request.new_access_token = new_access_token
                return None

        # TODO if two token is expired -> redirect to login

    def is_token_expired(self, *, access_token=None, refresh_token=None):
        try:
            if access_token:
                AccessToken(access_token)
            elif refresh_token:
                RefreshToken(refresh_token)
            else:
                return True
            return False
        except jwt.ExpiredSignatureError:
            return True
        except jwt.InvalidTokenError:
            return True

    def refresh_access_token(self, refresh_token):
        url = "http://127.0.0.1:8000/api/token/refresh/"
        response = requests.post(url, json={"refresh": refresh_token})

        if response.status_code == 200:
            return response.json().get("access")
        return None

