from django.db import models
from django.contrib.auth.models import AbstractUser


class StudentGroup(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class User(AbstractUser):

    role = models.CharField("Роль", max_length=15, default='student')
    tel = models.CharField("Телефон", max_length=15, blank=True)
    group_number = models.ForeignKey(StudentGroup, on_delete=models.PROTECT, null=True, blank=True)

    REQUIRED_FIELDS = ['first_name', 'last_name', 'email', 'role', 'tel', 'group_number']

    def __str__(self):
        return self.username
