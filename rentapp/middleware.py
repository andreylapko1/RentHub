import requests
from django.http import JsonResponse
from rest_framework_simplejwt.authentication import JWTAuthentication
from rentapp import settings

import requests
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings


import requests
import jwt
import datetime
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings

class AutoRefreshJWTMiddleware(MiddlewareMixin):
    def process_request(self, request):
        access_token = request.COOKIES.get("access_token")
        refresh_token = request.COOKIES.get("refresh_token")

        if access_token:
            request.META["HTTP_AUTHORIZATION"] = f"Bearer {access_token}"

        if access_token and self.is_token_expired(access_token) and refresh_token:
            new_access_token = self.refresh_access_token(refresh_token)
            if new_access_token:
                request.META["HTTP_AUTHORIZATION"] = f"Bearer {new_access_token}"
                request.COOKIES["access_token"] = new_access_token

    def is_token_expired(self, token):
        try:
            decoded = jwt.decode(token, settings.SIMPLE_JWT["SIGNING_KEY"], algorithms=["HS256"])
            return decoded["exp"] < datetime.datetime.utcnow().timestamp()
        except jwt.ExpiredSignatureError:
            return True
        except jwt.InvalidTokenError:
            return False

    def refresh_access_token(self, refresh_token):
        url = "http://127.0.0.1:8000/api/token/refresh/"
        response = requests.post(url, json={"refresh": refresh_token})

        if response.status_code == 200:
            return response.json().get("access")
        return None

