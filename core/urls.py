from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView
from .jwt_token import CustomTokenRefreshView
from users.reset_password import ResetPasswordView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from drf_yasg.generators import OpenAPISchemaGenerator
from rest_framework_extensions.routers import NestedRouterMixin
from users.views import UserViewSet, ChangePasswordView
from core.views import CustomLogoutView
from django.conf import settings
from django.conf.urls.static import static

class BothHttpAndHttpsSchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        schema = super().get_schema(request, public)
        schema.schemes = ["https", "http"]
        return schema

schema_view = get_schema_view(
    openapi.Info(
        title="core",
        default_version='v1',
        description="core",
        terms_of_service="",
        contact=openapi.Contact(email="kevin.a.g.97hotmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.IsAuthenticatedOrReadOnly],
    generator_class=BothHttpAndHttpsSchemaGenerator
)

class NestedDefaultRouter(NestedRouterMixin, DefaultRouter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.trailing_slash = '/?'

ROUTER = NestedDefaultRouter()
ROUTER.register('users', UserViewSet, basename='users')
#ROUTER.register('import-data', ImportDataViewSet, basename='import-data')
#ROUTER.register('pacientes', PacientesViewSet, basename='pacientes')

urlpatterns = [
    path('api/v1/users/create/', UserViewSet.as_view({'post': 'create'}), name='user-create'),
    path('admin/', admin.site.urls),
    path('api/v1/', include(ROUTER.urls)),
    path('api/v1/auth/logout/', CustomLogoutView.as_view(), name='logout'),
    path('api/v1/auth/', include('rest_framework.urls')),
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/reset-password/', ResetPasswordView.as_view()),
    path('api/v1/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/v1/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/v1/change-password/', ChangePasswordView.as_view(), name='change-password')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)