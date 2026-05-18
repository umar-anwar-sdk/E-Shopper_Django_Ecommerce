from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from django.conf import settings


def get_tokens_for_user(user):
    """
    Generate access and refresh tokens for a user
    """
    refresh = RefreshToken.for_user(user)
    
    # Add custom claims to tokens
    refresh['email'] = user.email
    refresh['role'] = user.role
    
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


def send_verification_email(user, email_token):
    """
    Send email verification email to user
    """
    verification_url = f"{settings.FRONTEND_URL}/verify-email/{email_token}"
    
    subject = 'Verify Your Email - E-Shopper'
    message = f'''
    Hello {user.first_name},
    
    Thank you for registering with E-Shopper!
    
    Please verify your email by clicking the link below:
    {verification_url}
    
    If you didn't create this account, please ignore this email.
    
    Best regards,
    E-Shopper Team
    '''
    
    try:
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Failed to send email: {str(e)}")
        return False


def send_welcome_email(user, password=None):
    """
    Send welcome email to user (especially for vendor creation by admin)
    """
    subject = 'Welcome to E-Shopper'
    
    if password:
        message = f'''
        Hello {user.first_name} {user.last_name},
        
        Your account has been created on E-Shopper!
        
        Login Details:
        Email: {user.email}
        Temporary Password: {password}
        
        Please change your password after first login.
        
        Best regards,
        E-Shopper Team
        '''
    else:
        message = f'''
        Hello {user.first_name},
        
        Welcome to E-Shopper!
        
        Your account has been created successfully.
        
        Best regards,
        E-Shopper Team
        '''
    
    try:
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Failed to send email: {str(e)}")
        return False


def send_password_reset_email(user, reset_token):
    """
    Send password reset email to user
    """
    reset_url = f"{settings.FRONTEND_URL}/reset-password/{reset_token}"
    
    subject = 'Reset Your Password - E-Shopper'
    message = f'''
    Hello {user.first_name},
    
    We received a request to reset your password.
    
    Click the link below to reset your password:
    {reset_url}
    
    This link will expire in 24 hours.
    
    If you didn't request this, please ignore this email.
    
    Best regards,
    E-Shopper Team
    '''
    
    try:
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Failed to send email: {str(e)}")
        return False
