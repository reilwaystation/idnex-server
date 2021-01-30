from django.db import models
from imagekit.models.fields import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.utils import timezone


class Person(models.Model):
    email = models.EmailField(max_length=255, unique=True)
    firstname = models.CharField(max_length=255, unique=False, blank=False)
    lastname = models.CharField(max_length=255, unique=False, blank=False)
    middlename = models.CharField(max_length=255, unique=False)
    extension = models.CharField(max_length=255, unique=False)
    birthdate = models.DateTimeField(default=timezone.now)
    birthplace = models.CharField(max_length=255, unique=False)
    status = models.CharField(max_length=255, unique=False)
    gender = models.CharField(max_length=255, unique=False)
    phone = models.IntegerField(default=0)
    nationality = models.CharField(max_length=255, unique=False)
    spouse = models.ForeignKey(
        'self', blank=True, on_delete=models.SET_NULL, null=True)
    thumbnail = ProcessedImageField(
        upload_to='profiles',
        processors=[ResizeToFill(256, 256)],
        format='JPEG',
        options={'quality': 72})

    def __str__(self):
        return f"{self.firstname} {self.lastname}"


class Address(models.Model):
    number = models.IntegerField(default=0)
    street = models.CharField(max_length=255, unique=True)
    barangay = models.CharField(max_length=255, unique=False)
    city = models.CharField(max_length=255, unique=False)
    province = models.CharField(max_length=255, unique=False)
    classification = models.CharField(max_length=255, unique=False)
    longitude = models.FloatField(max_length=255, unique=False)
    latitude = models.FloatField(max_length=255, unique=False)

    def __str__(self):
        return self.barangay


class Ownership(models.Model):
    owner = models.ForeignKey(Person, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    classification = models.CharField(max_length=255, unique=False)
    price = models.FloatField(max_length=255, unique=False)
    previous = models.FloatField(max_length=255, unique=False)
    acquired = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.owner.firstname} {self.owner.lastname}"
