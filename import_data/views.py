from rest_framework import status, viewsets
from rest_framework.viewsets import  mixins, GenericViewSet
from rest_framework_extensions.mixins import NestedViewSetMixin
from django_filters import rest_framework as filters
import django_filters
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
import pandas as pd
from .models import ImportData
from .serializers import ImportDataSerializer
from datetime import datetime


class ImportDataFilter(django_filters.FilterSet):
    paciente = django_filters.CharFilter(field_name="paciente", lookup_expr='unaccent__icontains')

    class Meta:
        model = ImportData
        fields = ['paciente']

class ImportDataViewSet(NestedViewSetMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, GenericViewSet):
    queryset = ImportData.objects.all()
    serializer_class = ImportDataSerializer
    parser_classes = (MultiPartParser, FormParser)
    filterset_class = ImportDataFilter

    def calculate_age(self, birthdate):
        if birthdate:
            today = datetime.today().date()
            return today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
        return None

    def parse_date(self, date_str):
        if pd.isna(date_str) or date_str in ['nan', 'NaT', '', 'None']:
            return None

        date_formats = [
            '%d/%m/%y', '%d-%m-%y %H:%M:%S', '%d-%m-%Y', '%d-%b-%y', 
            '%d-%b-%Y', '%Y-%m-%d', '%Y-%m-%d %H:%M:%S', '%d/%m/%Y'
        ]
        for date_format in date_formats:
            try:
                parsed_date = datetime.strptime(date_str, date_format).date()
                print(f"Successfully parsed {date_str} as {parsed_date} using format {date_format}")
                return parsed_date
            except (ValueError, TypeError):
                continue
        print(f"Failed to parse {date_str}")
        return None

    def get_int_value(self, value):
        try:
            if pd.isna(value) or value in ['nan', 'NaT', '', 'None']:
                return None
            return int(value)
        except (ValueError, TypeError):
            return None

    def get_decimal_value(self, value):
        try:
            if pd.isna(value) or value in ['nan', 'NaT', '', 'None']:
                return None
            return float(value)
        except (ValueError, TypeError):
            return None

    def get_str_value(self, value):
        if pd.isna(value) or value in ['nan', 'NaT', '', 'None']:
            return None
        return str(value)

    def create(self, request, *args, **kwargs):
        file = request.FILES.get('file')
        if not file:
            return Response({"detail": "No file provided."}, status=status.HTTP_400_BAD_REQUEST)

        # Verificar a extensão do arquivo
        if file.name.endswith('.csv'):
            df = pd.read_csv(file, delimiter=';')
        elif file.name.endswith('.xlsx'):
            df = pd.read_excel(file, engine='openpyxl')
        else:
            return Response({"detail": "Unsupported file format."}, status=status.HTTP_400_BAD_REQUEST)

        instances = []
        for _, row in df.iterrows():
            # Pular registros onde 'Paciente' é nulo ou vazio
            if pd.isna(row['Paciente']) or row['Paciente'] in ['nan', 'NaT', '', 'None']:
                continue

            # Converter a data de nascimento
            date_str = str(row['Data nascto'])
            print(f"Parsing date for {row['Paciente']}: {date_str}")
            data_nascimento = self.parse_date(date_str)

            print(f"Parsed date for {row['Paciente']}: {data_nascimento}")

            age = self.calculate_age(data_nascimento)

            instance = ImportData(
                paciente=self.get_str_value(row['Paciente']),
                endereco=self.get_str_value(row['Endereço']),
                cidade=self.get_str_value(row['Cidade']),
                profissao=self.get_str_value(row['Profissão']),
                telefone=self.get_str_value(row['Telefone']),
                data_nascimento=data_nascimento,
                sexo=self.get_str_value(row['Sexo']),
                cor=self.get_str_value(row['Cor']),
                observacoes=self.get_str_value(row['Observações']),
                historico=self.get_str_value(row['Histórico']),
                profissao2=self.get_str_value(row['Profissão2']),
                anos=self.get_int_value(row['Anos']),
                paciente1=self.get_str_value(row['paciente1']),
                data_consulta=self.parse_date(str(row['Data consulta'])),
                queixas=self.get_str_value(row['Queixas']),
                antecedentes1=self.get_str_value(row['Abtecedentes1']),
                antecedentes2=self.get_str_value(row['Antecedentes2']),
                antecedentes3=self.get_str_value(row['Antecedentes3']),
                situacao_social=self.get_str_value(row['Situação social']),
                idade2=self.get_int_value(row['Idade2']),
                peso=self.get_decimal_value(row['Peso']),
                altura=self.get_decimal_value(row['Altura']),
                aspectos=self.get_str_value(row['Aspectos']),
                ritmo=self.get_str_value(row['Ritmo']),
                bulhas=self.get_str_value(row['Bulhas']),
                sopros=self.get_str_value(row['Sopros']),
                pressao=self.get_str_value(row['Pressão']),
                pulso=self.get_str_value(row['Pulso']),
                aparelho_respiratorio=self.get_str_value(row['Aparelho Respiratório']),
                abdomem=self.get_str_value(row['Abdomem']),
                tireoide=self.get_str_value(row['Tireóide']),
                hipotese_diagnostico=self.get_str_value(row['Hipótese diagnostico']),
                idade3=self.get_int_value(row['Idade3']),
                age=age
            )
            instances.append(instance)

        ImportData.objects.bulk_create(instances)

        return Response(status=status.HTTP_201_CREATED)
