from django.db import migrations, models
from users.models import CustomUser, ProfileType
from django.contrib.auth import get_user_model

def create_profiles_and_users(apps, schema_editor):
    exists = ProfileType.objects.filter(profile_type=1).exists()
    if not exists:
        ProfileType.objects.create(profile_type=ProfileType.ADMIN)

    exists = ProfileType.objects.filter(profile_type=2).exists()
    if not exists:
        ProfileType.objects.create(profile_type=ProfileType.GUEST)
        
    exists = CustomUser.objects.filter(email='casani@recepcionista.com').exists()
    if not exists:
        User = get_user_model()
        guest_profile_type = ProfileType.objects.get(profile_type=ProfileType.GUEST)
        user = User.objects.create_user(
            first_name='Convidado',
            last_name='Convidado',
            email='convidado@convidado.com',
            password='senha123',
        )
        user.profile_type.add(guest_profile_type)  # Use add() para adicionar o perfil ao usuário
        user.save()
        
    exists = CustomUser.objects.filter(email='casani@admin.com').exists()
    if not exists:
        User = get_user_model()
        admin_profile_type = ProfileType.objects.get(profile_type=ProfileType.ADMIN)
        user = User.objects.create_superuser(
            first_name='Kevin',
            last_name='Garcia',
            email='kevin.a.g.97@hotmail.com',
            password='senha123',
            is_superuser = True,
        )
        user.profile_type.add(admin_profile_type)
        user.save()


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_profiles_and_users)
    ]
