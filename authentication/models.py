from django.db import models
from django.utils import timezone
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from imagekit.models.fields import ProcessedImageField
from imagekit.processors import ResizeToFill


class CustomUserManager(BaseUserManager):
    def _create_user(self, email, username, first_name, last_name, password, is_active, is_staff, is_superuser, **extra_fields):
        if not email:
            raise ValueError('Email is required')

        if not email:
            raise ValueError('Username is required')

        if not first_name:
            raise ValueError('First Name is required')

        if not last_name:
            raise ValueError('Last Name is required')

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name,
            is_staff=is_staff,
            is_superuser=is_superuser,
            is_active=is_active,
            last_login=timezone.now(),
            date_joined=timezone.now(),
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_user(self, email, username, first_name, last_name, password=None, **extra_fields):
        return self._create_user(email, username, first_name, last_name, password, False, False, False, **extra_fields)

    def create_superuser(self, email, username, first_name, last_name, password=None, **extra_fields):
        return self._create_user(email, username, first_name, last_name, password, True, True, True, **extra_fields)


class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255, unique=False)
    thumbnail = ProcessedImageField(
        default="profiles/default_zycnhz.jpg",
        upload_to='profiles',
        processors=[ResizeToFill(256, 256)],
        format='JPEG',
        options={'quality': 72})
    about = models.TextField(max_length=5000, blank=True, null=True)
    last_name = models.CharField(max_length=255, unique=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = CustomUserManager()

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        return True


class Ticket(models.Model):
    ticket = models.CharField(max_length=255, unique=True)
    exp = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.ticket


class Token(models.Model):
    token = models.CharField(max_length=255, unique=True)
    exp = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.token
