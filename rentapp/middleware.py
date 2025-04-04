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
from django.http import JsonResponse
from django.utils import timezone
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from django.utils.deprecation import MiddlewareMixin

class JWTAuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        access_token = request.COOKIES.get('access_token')
        refresh_token = request.COOKIES.get('refrest_token')

        if access_token:
            try:
                AccessToken(access_token)
                request.META['HTTP_AUTHORIZATION'] = f'Bearer {access_token}'
            except TokenError:
                if refresh_token:
                    new_access_token, new_refresh_token = self.refresh_access_token(refresh_token)
                    if new_access_token:
                        self.set_access_token_cookie(request, new_access_token)
                        self.set_refresh_token_cookie(request, new_refresh_token)
                        request.META['HTTP_AUTHORIZATION'] = f'Bearer {new_access_token}'
                    else:
                        request.COOKIES.pop('access_token', None)
                        request.COOKIES.pop('refresh_token', None)
                        return JsonResponse({"detail": "Token is expired or invalid"}, status=401)
                else:
                    request.COOKIES.pop('access_token', None)
                    return JsonResponse({"detail": "Access token expired and refresh token is missing."}, status=401)
        return None

    def refresh_access_token(self, refresh_token):
        try:
            refresh = RefreshToken(refresh_token)
            return str(refresh.access_token), refresh
        except TokenError:
            return None, None


    def set_access_token_cookie(self, request, new_access_token):
        response = request
        new_access_token_live = AccessToken(new_access_token)['exp'] - timezone.now().timestamp()
        response.set_cookie(
            key='access_token',
            value=new_access_token,
            httponly=True,
            secure=False,
            samesite='Lax',
            max_age=new_access_token_live
        )
        print('\n\nAAAAAAA',new_access_token_live)

    def set_refresh_token_cookie(self, request, new_refresh_token):
        response = request
        new_refresh_token_live = RefreshToken(new_refresh_token)['exp'] - timezone.now().timestamp()
        response.set_cookie(
            key='refresh_token',
            value=new_refresh_token,
            httponly=True,
            secure=False,
            samesite='Lax',
            max_age=new_refresh_token_live
        )