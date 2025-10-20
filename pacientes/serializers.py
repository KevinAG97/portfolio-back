from rest_framework import serializers
from .models import Pacientes
from .mixins import NestedCreateMixin, NestedUpdateMixin
from datetime import date

class PacientesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pacientes
        fields = [
            'id',
            'paciente', 
            'endereco', 
            'cidade', 
            'profissao', 
            'telefone', 
            'data_nascimento', 
            'sexo', 
            'cor', 
            'observacoes', 
            'historico', 
            'profissao2',
            'data_consulta', 
            'queixas', 
            'antecedentes1', 
            'antecedentes2', 
            'antecedentes3', 
            'situacao_social',
            'peso', 
            'altura', 
            'aspectos', 
            'ritmo', 
            'bulhas', 
            'sopros', 
            'pressao', 
            'pulso', 
            'aparelho_respiratorio', 
            'abdomem', 
            'tireoide', 
            'hipotese_diagnostico',
            'age',
            'created_at'
        ]

class CreatePacientesSerializer(NestedCreateMixin, NestedUpdateMixin, serializers.ModelSerializer):
    class Meta:
        model = Pacientes
        fields = ['id', 'paciente', 'data_nascimento', 'sexo', 'cor', 'endereco', 'cidade', 'profissao', 'telefone', 'age']
        read_only_fields = ['id', 'age']

    def create(self, validated_data):
        data_nascimento = validated_data.get('data_nascimento', None)
        if data_nascimento:
            today = date.today()
            age = today.year - data_nascimento.year - ((today.month, today.day) < (data_nascimento.month, data_nascimento.day))
            validated_data['age'] = age
        else:
            validated_data['age'] = None

        # Define data_consulta como a data atual
        validated_data['data_consulta'] = date.today()

        return super().create(validated_data)