from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
import datetime
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
# Create your views here.

class CustomLoginView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        print(response.data)
        response.set_cookie(
            key="refreshToken", 
            value=response.data["refresh"],
            expires=datetime.datetime.now() + datetime.timedelta(days=1),
            path="/",secure=True,
            httponly=True
        )
        del response.data["refresh"]
        return response


class CustomTokenRefreshView(TokenRefreshView):
    """
    Custom view to refresh the access token using the refresh token from
    the HttpOnly cookie.
    """
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get(settings.SIMPLE_JWT['AUTH_COOKIE'])

        if refresh_token is None:
            return Response({"detail": "Refresh token not found in cookies."},
                            status=status.HTTP_401_UNAUTHORIZED)

        # Inject the refresh token into the request data
        request.data['refresh'] = refresh_token
        response = super().post(request, *args, **kwargs)

        return response