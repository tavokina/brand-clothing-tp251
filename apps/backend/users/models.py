from django.contrib.auth.models import (AbstractUser,
                                        UserManager)
from django.db import models

class CustomUserManager(UserManager):
    def create_user(self, email=None, password=None, **extra_fields):
        if not email:
            raise ValueError("User must have an email address")
        email = self.normalize_email(email)
        extra_fields.setdefault("username", email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if not email:
            raise ValueError("Superuser must have an email address")

        return self.create_user(email=email, password=password, **extra_fields)


class User(AbstractUser):
    email = models.EmailField(unique=True)
    age = models.PositiveSmallIntegerField(null=True, blank=True)

    marketing_opt_in = models.BooleanField(default=False)
    instagram = models.TextField()

    phone_number = models.CharField(max_length=20, blank=True)
    is_active = models.BooleanField(default=False)

    name = models.TextField(blank=True)


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()
