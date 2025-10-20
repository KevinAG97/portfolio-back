from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.request import Request
from rest_framework.response import Response
from users.models import CustomUser
from django.utils import timezone
from rest_framework_simplejwt.tokens import AccessToken

class CustomTokenRefreshView(TokenRefreshView):
    
    def post(self, request: Request, *args, **kwargs) -> Response:
        response = super().post(request, *args, **kwargs)
        try:
            token = AccessToken(token=response.data['access'], verify=False)
            user_id = token.payload['user_id']
            CustomUser.objects.filter(id=user_id).update(last_login=timezone.now())
        except:
            pass
        return response
