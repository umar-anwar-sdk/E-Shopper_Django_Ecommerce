from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import CustomUser, TokenBlacklist


@receiver(post_save, sender=CustomUser)
def user_created_signal(sender, instance, created, **kwargs):
    """
    Signal triggered when a new user is created
    """
    if created:
        # You can add additional logic here
        # For example: send welcome email, create user profile, etc.
        pass


# Clean up expired tokens periodically
def cleanup_expired_tokens():
    """
    Remove expired tokens from blacklist
    This can be called periodically by a background task
    """
    TokenBlacklist.objects.filter(expires_at__lt=timezone.now()).delete()
