from django.contrib.auth.views import LogoutView
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator


class CustomLogoutView(LogoutView):
  
    http_method_names = ["get", "head", "post", "options"]
   
    @method_decorator(csrf_protect)
    def get(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)