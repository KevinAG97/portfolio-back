from .models import *
from .serializers import *

from rest_framework.viewsets import GenericViewSet, mixins
from rest_framework_extensions.mixins import NestedViewSetMixin
from users.decorators import tag_all_views
from django.contrib.auth.hashers import make_password
from django.http import QueryDict
from rest_framework import status
from rest_framework.response import Response

from users.decorators import tag_all_views
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login
from rest_framework.response import Response
from django.core.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny

@tag_all_views('Usuários')
class UserViewSet(NestedViewSetMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, GenericViewSet):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateUserSerializer
        else:
            return UserSerializer
        
    def get_queryset(self):
        user = self.request.user
        queryset = CustomUser.objects.filter(id=user.id)
        return queryset         
    
    def create(self, request, *args, **kwargs):
        email = request.data.get('email', None)
        if email:
            exists_email = CustomUser.objects.filter(email=email).exists()
            if exists_email:
                return Response({'error': 'E-mail já cadastrado.'}, status=status.HTTP_409_CONFLICT)
            
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            mutable_request_data = request.data.copy()
            mutable_request_data['password'] = make_password(serializer.validated_data['password'])
            
            serializer = self.get_serializer(data=mutable_request_data)
            if serializer.is_valid(raise_exception=True):
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        password = request.data.get('password')
        if password:
            request.data['password'] = make_password(password)
        return super(UserViewSet, self).update(request, *args, **kwargs)
    
@tag_all_views('Tipos De Usuários')
class ProfileTypeViewSet(NestedViewSetMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, GenericViewSet):
    queryset = ProfileType.objects.all()
    serializer_class = ProfileTypeSerializer
    

class ChangePasswordView(APIView):
    
    def post(self, request, *args, **kwargs):
        user = request.user 
        if not request.user.is_authenticated:
            raise PermissionDenied("Acesso negado. Faça login para alterar a senha.")
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            old_password = serializer.validated_data['old_password']
            new_password1 = serializer.validated_data['new_password1']
            new_password2 = serializer.validated_data['new_password2']

            user = request.user
            if not user.check_password(old_password):
                return Response({'error': 'Senha antiga incorreta.'}, status=status.HTTP_400_BAD_REQUEST)

            if new_password1 != new_password2:
                return Response({'error': 'As novas senhas não coincidem.'}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(new_password1)
            user.save()
            
            # Reautenticar o usuário
            user = authenticate(request, username=user.email, password=new_password1)
            if user is not None:
                login(request, user)
                return Response({'message': 'Senha alterada com sucesso.'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Erro ao reautenticar o usuário.'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
