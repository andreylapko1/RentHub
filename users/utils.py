from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken



def set_jwt_token(user, response):
    if response is None:
        response = Response(status=status.HTTP_200_OK)

    refresh_token = RefreshToken.for_user(user)
    access_token = refresh_token.access_token

    refresh_token_live = refresh_token['exp'] - timezone.now().timestamp()
    access_token_live = access_token['exp'] - timezone.now().timestamp()

    response.set_cookie(
        key='refresh_token',
        value=str(refresh_token),
        httponly=True,
        secure=False,
        samesite='Lax',
        max_age=refresh_token_live)

    response.set_cookie(
        key='access_token',
        value=str(access_token),
        httponly=True,
        secure=False,
        samesite='Lax',
        max_age=access_token_live
    )
    return response