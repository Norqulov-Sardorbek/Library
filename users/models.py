from random import choices

from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from users.managers import UserManager

class UserRole(models.TextChoices):
    Admin="Admin",'Admin'
    User="User",'User'
    Operator="Operator",'Operator'

class CustomUser(AbstractUser):
    username = models.CharField(max_length=100, unique=True)
    role = models.CharField(max_length=20, choices=UserRole, default=UserRole.User)
    created_at = models.DateField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateField(auto_now=True, null=True, blank=True)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    groups = models.ManyToManyField(Group, related_name="customuser_groups", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="customuser_permissions", blank=True)
    objects = UserManager()


    def __str__(self):
        return self.username
