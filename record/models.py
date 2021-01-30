from django.db import models
from imagekit.models.fields import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.utils import timezone


class Person(models.Model):
    email = models.EmailField(max_length=255, blank=True, null=True)
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    middlename = models.CharField(max_length=255, blank=True, null=True)
    extension = models.CharField(max_length=255, blank=True, null=True)
    birthdate = models.DateTimeField(blank=True, null=True)
    birthplace = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=255, blank=True, null=True)
    gender = models.CharField(max_length=255, blank=True, null=True)
    phone = models.IntegerField(default=0, blank=True, null=True)
    nationality = models.CharField(max_length=255, blank=True, null=True)
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
    number = models.IntegerField(default=0, null=True, blank=True)
    street = models.CharField(max_length=255, null=True, blank=True)
    barangay = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    province = models.CharField(max_length=255)
    classification = models.CharField(max_length=255,  null=True, blank=True)
    longitude = models.FloatField(max_length=255,  null=True, blank=True)
    latitude = models.FloatField(max_length=255,  null=True, blank=True)

    def __str__(self):
        return f"{self.barangay}, {self.city}, {self.province}"


class Ownership(models.Model):
    owner = models.ForeignKey(Person, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    classification = models.CharField(max_length=255, unique=False)
    price = models.FloatField(max_length=255, unique=False)
    previous = models.FloatField(max_length=255, unique=False)
    acquired = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.owner.firstname} {self.owner.lastname}"
