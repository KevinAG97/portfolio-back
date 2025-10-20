from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
import time

class UserManager(BaseUserManager):

    def create_user(self, email: str,first_name: str, last_name: str, password: str=None, is_staff=False, is_superuser=False, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        if not first_name:
            raise ValueError('Users must have a first name')
        if not last_name:
            raise ValueError('Users must have a last name')

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            is_staff=is_staff,
            is_superuser=is_superuser,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email: str, first_name: str, last_name: str, password: str=None, is_staff=True, is_superuser=True, **extra_fields):
        user = self.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            is_staff=True,
            is_superuser=True,
            **extra_fields
        )
        user.save()
        return user
    
class ProfileType(models.Model):
    ADMIN = 1
    GUEST = 2

    ROLE_CHOICES = (
      (ADMIN, 'admin'),
      (GUEST, 'guest')
  )

    profile_type = models.PositiveSmallIntegerField(choices=ROLE_CHOICES)
    
def user_photo(instance, filename):
    photo_id = str(instance.id)
    url = f'user_photo/{photo_id}/{str(time.time() * 1000) + filename}'
    return url


class CustomUser(AbstractUser):
    first_name = models.CharField(verbose_name='First Name', max_length=255)
    last_name = models.CharField(verbose_name='Last Name', max_length=255)
    email = models.EmailField(verbose_name='Email', max_length=255, unique=True)
    username = None
    date_joined = models.DateTimeField(auto_now_add=True)
    profile_type = models.ManyToManyField(ProfileType, blank=False, related_name='user_profile_type')
    photo = models.ImageField(upload_to=user_photo, blank=True, null=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()