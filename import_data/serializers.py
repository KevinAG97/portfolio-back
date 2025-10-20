from rest_framework import serializers
from .models import ImportData

class ImportDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImportData
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
            'age'
        ]