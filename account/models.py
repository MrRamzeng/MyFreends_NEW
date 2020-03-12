from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from account.managers import CustomStaffManager


def user_photo(instance, filename):
    return "%s/photo/%s" % (instance.username, filename)


class Account(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField('Логин', max_length=254, unique=True)
    first_name = models.CharField('Имя', max_length=50)
    last_name = models.CharField('Фамилия', max_length=50)
    photo = models.ImageField(
        'Фото', upload_to=user_photo, default='avatar.png'
    )
    is_active = models.BooleanField(_("active"), default=False)
    is_staff = models.BooleanField(_("staff"), default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', 'first_name', 'last_name')
    objects = CustomStaffManager()
    
    class Meta:
        verbose_name = _("account")
        verbose_name_plural = _("accounts")

    def __str__(self):
        return (str(self.first_name) + ' ' + str(self.last_name))


@receiver(post_save, sender=User)
def create_account(sender, instance, created, **kwargs):
    if created:
        Account.objects.create(email=instance)


@receiver(post_save, sender=User)
def save_account(sender, instance, **kwargs):
    instance.user.save()
