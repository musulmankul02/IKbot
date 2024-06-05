from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    age = models.PositiveIntegerField(blank=True, null=True)

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    region = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    checkout_date = models.DateField()
    comment = models.TextField()
    number_of_people = models.IntegerField()
    amenities = models.JSONField(default=list, blank=True)
    distance_to_beach = models.IntegerField(default=0, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    price = models.IntegerField(default=0)
    photos = models.TextField()  # Сохранение фото как списка file_id через запятую

class Invitation(models.Model):
    user = models.ForeignKey(User, related_name='invitations', on_delete=models.CASCADE)
    invited_by = models.ForeignKey(User, related_name='invited_users', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

class UserBusness(models.Model):
    user_id = models.IntegerField(primary_key=True)
    referral_status = models.IntegerField(default=0)
    referrer_id = models.IntegerField(null=True, blank=True)

class Hotel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    description = models.TextField()
    allocation_type = models.CharField(max_length=50)
    places = models.CharField(max_length=50)
    facilities = models.TextField()
    distance = models.CharField(max_length=50)
    price = models.CharField(max_length=50)
    photos = models.TextField()  # Сохранение фото как списка file_id через запятую

class District(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Pension(models.Model):
    name = models.CharField(max_length=100)
    district = models.ForeignKey(District, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class AccommodationType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
