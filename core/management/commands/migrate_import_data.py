from django.core.management.base import BaseCommand
from import_data.models import ImportData  
from pacientes.models import Pacientes

class Command(BaseCommand):
    help = 'Migra dados de import_data para pacientes'

    def handle(self, *args, **kwargs):
        # Obtendo todos os registros de import_data
        import_data_records = ImportData.objects.all()
        
        # Iterando sobre os registros e migrando para Pacientes
        for record in import_data_records:
            Pacientes.objects.create(
                paciente=record.paciente,
                endereco=record.endereco,
                cidade=record.cidade,
                profissao=record.profissao,
                telefone=record.telefone,
                data_nascimento=record.data_nascimento,
                sexo=record.sexo,
                cor=record.cor,
                observacoes=record.observacoes,
                historico=record.historico,
                profissao2=record.profissao2,
                anos=record.anos,
                data_consulta=record.data_consulta,
                queixas=record.queixas,
                antecedentes1=record.antecedentes1,
                antecedentes2=record.antecedentes2,
                antecedentes3=record.antecedentes3,
                situacao_social=record.situacao_social,
                idade2=record.idade2,
                peso=record.peso,
                altura=record.altura,
                aspectos=record.aspectos,
                ritmo=record.ritmo,
                bulhas=record.bulhas,
                sopros=record.sopros,
                pressao=record.pressao,
                pulso=record.pulso,
                aparelho_respiratorio=record.aparelho_respiratorio,
                abdomem=record.abdomem,
                tireoide=record.tireoide,
                hipotese_diagnostico=record.hipotese_diagnostico,
                idade3=record.idade3,
                age=record.age
            )

        self.stdout.write(self.style.SUCCESS('Dados migrados com sucesso de import_data para pacientes.'))
