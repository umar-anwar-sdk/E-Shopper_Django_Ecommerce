import re
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import get_password_validators
from django.contrib.auth.password_validation import validate_password as django_validate_password


class PasswordValidator:
    """
    Custom password validator for strong password requirements
    """
    
    def __init__(self):
        self.min_length = 8
        self.require_uppercase = True
        self.require_lowercase = True
        self.require_digits = True
        self.require_special = True
    
    def validate(self, password):
        """
        Validate password against all requirements
        Returns (is_valid, error_message)
        """
        errors = []
        
        # Check minimum length
        if len(password) < self.min_length:
            errors.append(f'Password must be at least {self.min_length} characters long.')
        
        # Check for uppercase
        if self.require_uppercase and not re.search(r'[A-Z]', password):
            errors.append('Password must contain at least one uppercase letter.')
        
        # Check for lowercase
        if self.require_lowercase and not re.search(r'[a-z]', password):
            errors.append('Password must contain at least one lowercase letter.')
        
        # Check for digits
        if self.require_digits and not re.search(r'[0-9]', password):
            errors.append('Password must contain at least one digit.')
        
        # Check for special characters
        if self.require_special and not re.search(r'[!@#$%^&*()_+\-=\[\]{};:\'",.<>?/\\|`~]', password):
            errors.append('Password must contain at least one special character (!@#$%^&*...).')
        
        if errors:
            return False, ' '.join(errors)
        
        return True, None
    
    def __call__(self, password):
        """
        Callable validator for use in Django forms/models
        """
        is_valid, error_message = self.validate(password)
        if not is_valid:
            raise ValidationError(error_message)


class EmailValidator:
    """
    Custom email validator
    """
    
    EMAIL_PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    @staticmethod
    def validate(email):
        """
        Validate email format
        """
        if not re.match(EmailValidator.EMAIL_PATTERN, email):
            raise ValidationError('Invalid email format.')
        return True


# Create instance for easy import
password_validator = PasswordValidator()
