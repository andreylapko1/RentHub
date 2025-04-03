# class JWTAuthMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
#
#     def __call__(self, request):
#         access_token = request.COOKIES.get('access_token')
#         if access_token:
#             request.META['HTTP_AUTHORIZATION'] = f'Bearer {access_token}'
#         else:
#             request.META.pop('HTTP_AUTHORIZATION', None)
#
#         response = self.get_response(request)
#         return response
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from django.utils.deprecation import MiddlewareMixin

class JWTAuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        access_token = request.COOKIES.get('access_token')

        if access_token:
            try:
                AccessToken(access_token)
                request.META['HTTP_AUTHORIZATION'] = f'Bearer {access_token}'
            except TokenError:
                request.COOKIES.pop('access_token', None)
                request.COOKIES.pop('refresh_token', None)
                return None

        return None