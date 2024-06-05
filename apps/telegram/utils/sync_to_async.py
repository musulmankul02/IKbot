from apps.telegram.models import Booking, Invitation, Profile
from asgiref.sync import sync_to_async
from django.contrib.auth.models import User

@sync_to_async
def check_invitations(user_id):
    return Invitation.objects.filter(invited_by_id=user_id).count() >= 10

@sync_to_async
def get_invitation_count(user_id):
    return Invitation.objects.filter(invited_by_id=user_id).count()

@sync_to_async
def create_booking(user, region, city, checkout_date, comment):
    Booking.objects.create(user=user, region=region, city=city, checkout_date=checkout_date, comment=comment)

@sync_to_async
def get_user(user_id):
    return User.objects.filter(id=user_id).first()

@sync_to_async
def create_invitation(user_id, invited_by_id):
    Invitation.objects.create(user_id=user_id, invited_by_id=invited_by_id)

@sync_to_async
def create_user(user_id, username):
    return User.objects.create(id=user_id, username=username)

@sync_to_async
def create_or_get_profile(user):
    return Profile.objects.get_or_create(user=user)

@sync_to_async
def profile_exists(user_id):
    return Profile.objects.filter(user_id=user_id).exists()