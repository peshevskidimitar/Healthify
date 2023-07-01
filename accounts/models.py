from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMINISTRATOR = 'ADMINISTRATOR', 'Administrator'
        CONSUMER = 'CONSUMER', 'Consumer'
        SELLER = 'SELLER', 'Seller'

    base_role = Role.ADMINISTRATOR

    role = models.CharField(max_length=255, choices=Role.choices)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.base_role

        return super().save(*args, **kwargs)


class ConsumerManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(role=User.Role.CONSUMER)


class Consumer(User):
    base_role = User.Role.CONSUMER
    objects = ConsumerManager()

    class Meta:
        proxy = True


class SellerManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(role=User.Role.SELLER)


class Seller(User):
    base_role = User.Role.SELLER
    objects = SellerManager()

    class Meta:
        proxy = True
