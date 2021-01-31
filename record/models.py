from django.db import models
from imagekit.models.fields import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.utils import timezone


class Person(models.Model):
    email = models.EmailField(max_length=255, blank=True)
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    middlename = models.CharField(max_length=255, blank=True)
    extension = models.CharField(max_length=255, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    birthplace = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=255, blank=True)
    gender = models.CharField(max_length=255, blank=True)
    phone = models.IntegerField(default=0, blank=True, null=True)
    nationality = models.CharField(max_length=255, blank=True)
    thumbnail = ProcessedImageField(
        upload_to='profiles',
        processors=[ResizeToFill(256, 256)],
        format='JPEG',
        options={'quality': 72},
        blank=True, null=True)
    spouse = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        blank=True,
        null=True)

    def __str__(self):
        return f"{self.firstname} {self.lastname}"


class Address(models.Model):
    number = models.IntegerField(default=0, blank=True, null=True)
    street = models.CharField(max_length=255, blank=True)
    barangay = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    province = models.CharField(max_length=255)
    classification = models.CharField(max_length=255, blank=True)
    longitude = models.FloatField(max_length=255, blank=True)
    latitude = models.FloatField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.barangay}, {self.city}, {self.province}"


class Ownership(models.Model):
    owner = models.ForeignKey(Person, on_delete=models.CASCADE, null=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, null=True)
    classification = models.CharField(max_length=255, blank=True)
    price = models.FloatField(max_length=255, blank=True, null=True)
    previous = models.FloatField(max_length=255, blank=True, null=True)
    acquired = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.owner.firstname} {self.owner.lastname}"
