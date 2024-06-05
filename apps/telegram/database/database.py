from apps.telegram.models import Invitation

def check_invitations(user_id):
    return Invitation.objects.filter(invited_by_id=user_id).count() >= 10

# Получение количества приглашений
def get_invitation_count(user_id):
    return Invitation.objects.filter(invited_by_id=user_id).count()