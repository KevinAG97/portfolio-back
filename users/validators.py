import re
from rest_framework import serializers


def validate_first_name(first_name):
    nome_sem_espaco = first_name.replace(" ", "") 
    return nome_sem_espaco.isalpha()
        
def validate_last_name(last_name):
    nome_sem_espaco = last_name.replace(" ", "") 
    return nome_sem_espaco.isalpha()

def validate_password(value):
    # Validar se a senha contém pelo menos 8 caracteres, incluindo números e letras
    if len(value) < 8 or not any(char.isnumeric() for char in value) or not any(char.isalpha() for char in value):
        raise serializers.ValidationError("A senha deve ter pelo menos 8 caracteres e conter pelo menos um número e uma letra.")