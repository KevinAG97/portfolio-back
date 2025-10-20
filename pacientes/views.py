from rest_framework import viewsets
from .models import Pacientes
from .serializers import PacientesSerializer, CreatePacientesSerializer
from rest_framework.viewsets import  mixins, GenericViewSet
from rest_framework_extensions.mixins import NestedViewSetMixin
from django_filters import rest_framework as filters
import django_filters
from rest_framework.response import Response
from datetime import date, datetime
from django.db.models import Case, When, Value, BooleanField
from django.db.models import Value
from django.db.models.functions import Trim
from rest_framework.permissions import AllowAny

class PacientesFilter(django_filters.FilterSet):
    paciente = django_filters.CharFilter(field_name="paciente", lookup_expr='unaccent__icontains')
    id = filters.NumberFilter(field_name="id")

    class Meta:
        model = Pacientes
        fields = ['paciente', 'id']

class PacientesViewSet(NestedViewSetMixin, 
                       mixins.RetrieveModelMixin, 
                       mixins.ListModelMixin, 
                       mixins.CreateModelMixin, 
                       mixins.UpdateModelMixin, 
                       mixins.DestroyModelMixin, 
                       GenericViewSet):
    queryset = Pacientes.objects.all()
    serializer_class = PacientesSerializer
    filterset_class = PacientesFilter
    permission_classes = [AllowAny]

    def get_permissions(self):
        # Permitir acesso público a todas as ações
        return [AllowAny()]

    def get_serializer_class(self):
        if self.action == 'create':
            return CreatePacientesSerializer
        return PacientesSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        # Anotar com o nome sem espaços no início
        queryset = queryset.annotate(trimmed_name=Trim('paciente')).order_by('trimmed_name')
        return queryset
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        # Calcula a idade atual com base na data de nascimento
        if instance.data_nascimento:
            today = date.today()
            nova_idade = today.year - instance.data_nascimento.year - (
                (today.month, today.day) < (instance.data_nascimento.month, instance.data_nascimento.day)
            )

            # Se a idade armazenada estiver diferente, atualiza
            if instance.age != nova_idade:
                instance.age = nova_idade
                instance.save(update_fields=['age'])

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data.copy()

        # Se a data de nascimento for fornecida, calcula a idade
        data_nascimento_str = data.get('data_nascimento')
        if data_nascimento_str:
            try:
                # Convertendo a string para um objeto date
                data_nascimento = datetime.strptime(data_nascimento_str, '%Y-%m-%d').date()
                today = date.today()
                age = today.year - data_nascimento.year - ((today.month, today.day) < (data_nascimento.month, data_nascimento.day))
                data['age'] = age
            except ValueError:
                return Response({'error': 'Invalid date format. Expected YYYY-MM-DD.'}, status=400)

        # Atualiza a data da consulta para a data atual
        data['data_consulta'] = date.today()

        serializer = self.get_serializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)