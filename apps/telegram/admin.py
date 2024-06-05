# admin.py

from django.contrib import admin
from .models import District, Pension, AccommodationType, Booking, Invitation, UserBusness

admin.site.register(District)
admin.site.register(Pension)
admin.site.register(AccommodationType)
admin.site.register(Booking)
admin.site.register(Invitation)
admin.site.register(UserBusness)
