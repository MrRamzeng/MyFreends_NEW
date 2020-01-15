from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, User
from django.dispatch import receiver
from account.managers import StaffManager
from django.db.models.signals import post_save

class Account(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('Адрес электронной почты', max_length=254, unique=True)
    first_name = models.CharField('Имя', max_length=50)
    last_name = models.CharField('Фамилия', max_length=50)
    username = models.CharField('Логин', max_length=50, unique=True)
    is_active = models.BooleanField('Активный', default=False)
    is_staff = models.BooleanField('Администратор', default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', 'first_name', 'last_name')
    objects = StaffManager()

    class Meta:
        verbose_name = 'Учетная запись'
        verbose_name_plural = 'Учетные записи'

@receiver(post_save, sender=User)
def create_account(sender, instance, created, **kwargs):
    if created:
        Account.objects.create(email=instance)

@receiver(post_save, sender=User)
def save_account(sender, instance, **kwargs):
    instance.user.save()
