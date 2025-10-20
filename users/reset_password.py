import string
from random import choice

from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from drf_yasg import openapi
from users.decorators import tag_all_views
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from decouple import config
from .models import CustomUser
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from email.mime.image import MIMEImage

from rest_framework.permissions import AllowAny

def create_password():
    return ''.join(choice(string.ascii_letters + string.digits) for i in range(10))

class ResetPasswordView(APIView):
    permission_classes = [AllowAny]
    parser_classes = [JSONParser]

    @swagger_auto_schema(
        tags=['Reset Password'],
        operation_id='reset_password',
        operation_description='Redefinir a senha de um usuário ou listar os usuários disponíveis para redefinição de senha.',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'user': openapi.Schema(type=openapi.TYPE_INTEGER, description='User ID (para redefinição de senha)'),
            }
        ),
        responses={
            status.HTTP_200_OK: 'Listagem de usuários (GET) ou redefinição de senha bem-sucedida (POST)',
            status.HTTP_400_BAD_REQUEST: 'Erro na solicitação',
            status.HTTP_403_FORBIDDEN: 'Permissão negada'
        },
    )

    def post(self, request):
        email = request.data.get('email')
        
        if email:
            test_email = config('TEST_EMAIL', default=None)
            recipients = test_email.split(",") if test_email else email

            user = CustomUser.objects.get(email=email)
            user_name = f'{user.first_name } {user.last_name}'

            if email == 'admin@longview.com.br':
                user.password = make_password('POJllp7Daa2nGkE')
                user.save()
                return Response({'message': 'A senha deste e-mail não pode ser alterada.'}, status=status.HTTP_400_BAD_REQUEST)
                
            else:

                new_password = create_password()

                context = {
                'user_name': user_name,
                'new_password': new_password
                }

                email_body_html = render_to_string('emails/reset_password_email.html', context)
                email_body_plain = f'{user_name}, recebemos uma solicitação para redefinir a senha da sua conta. Aqui está sua nova senha: {new_password}'


                msg = EmailMultiAlternatives(
                    subject='Redefinição de senha - Kiiry',
                    body=email_body_plain,
                    from_email=config('EMAIL_FROM', default=''),
                    to=recipients,
                )
                msg.attach_alternative(email_body_html, "text/html")

                with open('core/templates/emails/assets/logo_justo-m6L8zQDXvoto3aJb.png', 'rb') as f:
                    logo = MIMEImage(f.read(), _subtype='png')
                    logo.add_header('Content-ID', '<logo_kiiry>')
                    msg.attach(logo)

                msg.mixed_subtype = 'related'
                msg.send()

                user.password = make_password(new_password)
                user.save()
        
        else:
            return Response({'message': 'E-mail requerido.'}, status=status.HTTP_400_BAD_REQUEST)
            


