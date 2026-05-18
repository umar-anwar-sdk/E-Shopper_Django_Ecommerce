from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser, TokenBlacklist
from .validators import password_validator, EmailValidator
from django.core.exceptions import ValidationError as DjangoValidationError


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for user profile information
    """
    role_display = serializers.CharField(source='get_role_display', read_only=True)
    
    class Meta:
        model = CustomUser
        fields = [
            'id', 'email', 'first_name', 'last_name', 'phone_number',
            'role', 'role_display', 'is_verified', 'created_at', 'updated_at',
            'shop_name', 'shop_description', 'bank_account'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'role', 'role_display']


class CustomerRegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for customer registration (role is automatically set to customer)
    """
    password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'},
        help_text='Password must be at least 8 characters with uppercase, lowercase, digits, and special characters.'
    )
    confirm_password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'},
        required=True,
        label='Confirm Password'
    )
    
    class Meta:
        model = CustomUser
        fields = [
            'email', 'first_name', 'last_name', 'phone_number',
            'password', 'confirm_password'
        ]
    
    def validate_email(self, value):
        """Validate email is unique and valid format"""
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email already exists. Please use a different email or login.')
        
        try:
            EmailValidator.validate(value.lower())
        except DjangoValidationError as e:
            raise serializers.ValidationError(str(e))
        
        return value.lower()
    
    def validate_first_name(self, value):
        """Validate first name"""
        if not value or len(value.strip()) == 0:
            raise serializers.ValidationError('First name cannot be empty.')
        return value.strip()
    
    def validate_last_name(self, value):
        """Validate last name"""
        if not value or len(value.strip()) == 0:
            raise serializers.ValidationError('Last name cannot be empty.')
        return value.strip()
    
    def validate(self, data):
        """Validate password fields"""
        password = data.get('password')
        confirm_password = data.pop('confirm_password', None)
        
        # Validate password strength
        is_valid, error_message = password_validator.validate(password)
        if not is_valid:
            raise serializers.ValidationError({'password': error_message})
        
        # Check if passwords match
        if password != confirm_password:
            raise serializers.ValidationError({
                'confirm_password': 'Passwords do not match. Please ensure both passwords are identical.'
            })
        
        return data
    
    def create(self, validated_data):
        """Create a new customer user"""
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone_number=validated_data.get('phone_number'),
            role='customer'  # Automatically set role to customer
        )
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom token serializer to include user information
    """
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        # Add custom claims
        token['email'] = user.email
        token['role'] = user.role
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        
        return token
    
    def validate(self, attrs):
        """
        Validate email and password for login
        """
        email = attrs.get('email')
        password = attrs.get('password')
        
        if email and password:
            user = authenticate(
                request=self.context.get('request'),
                username=email,
                password=password
            )
            
            if not user:
                raise serializers.ValidationError(
                    'Invalid email or password. Please check your credentials and try again.'
                )
        else:
            msg = 'Must include both "email" and "password".'
            raise serializers.ValidationError(msg)
        
        attrs['user'] = user
        return attrs


class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login
    """
    email = serializers.EmailField()
    password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'},
        required=True
    )
    
    def validate(self, data):
        """Validate login credentials"""
        email = data.get('email')
        password = data.get('password')
        
        user = authenticate(username=email, password=password)
        
        if not user:
            raise serializers.ValidationError(
                'Invalid email or password. Please check your credentials and try again.'
            )
        
        data['user'] = user
        return data


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for changing user password
    """
    old_password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'},
        required=True,
        label='Current Password'
    )
    new_password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'},
        required=True,
        label='New Password'
    )
    confirm_password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'},
        required=True,
        label='Confirm New Password'
    )
    
    def validate_new_password(self, value):
        """Validate new password strength"""
        is_valid, error_message = password_validator.validate(value)
        if not is_valid:
            raise serializers.ValidationError(error_message)
        return value
    
    def validate(self, data):
        """Validate all password fields"""
        user = self.context['request'].user
        
        # Check if old password is correct
        if not user.check_password(data['old_password']):
            raise serializers.ValidationError({
                'old_password': 'Current password is incorrect.'
            })
        
        # Check if new passwords match
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError({
                'confirm_password': 'New passwords do not match.'
            })
        
        # Ensure new password is different from old password
        if data['old_password'] == data['new_password']:
            raise serializers.ValidationError({
                'new_password': 'New password must be different from the current password.'
            })
        
        return data


class UpdateProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for updating user profile
    """
    class Meta:
        model = CustomUser
        fields = [
            'first_name', 'last_name', 'phone_number',
            'shop_name', 'shop_description', 'bank_account',
            'brand_logo', 'brand_banner'
        ]
    
    def validate_phone_number(self, value):
        """Validate phone number format"""
        if value and len(value) < 10:
            raise serializers.ValidationError('Phone number must be at least 10 digits.')
        return value


class VendorCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for admin to create vendors
    Only admins can use this serializer
    """
    password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'},
        required=True
    )
    
    class Meta:
        model = CustomUser
        fields = [
            'email', 'first_name', 'last_name', 'phone_number',
            'password', 'shop_name', 'shop_description', 'bank_account'
        ]
    
    def validate_email(self, value):
        """Validate email is unique"""
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email already exists.')
        
        try:
            EmailValidator.validate(value.lower())
        except DjangoValidationError as e:
            raise serializers.ValidationError(str(e))
        
        return value.lower()
    
    def validate_password(self, value):
        """Validate password strength"""
        is_valid, error_message = password_validator.validate(value)
        if not is_valid:
            raise serializers.ValidationError(error_message)
        return value
    
    def validate_first_name(self, value):
        """Validate first name"""
        if not value or len(value.strip()) == 0:
            raise serializers.ValidationError('First name cannot be empty.')
        return value.strip()
    
    def validate_last_name(self, value):
        """Validate last name"""
        if not value or len(value.strip()) == 0:
            raise serializers.ValidationError('Last name cannot be empty.')
        return value.strip()
    
    def create(self, validated_data):
        """Create a new vendor user"""
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone_number=validated_data.get('phone_number'),
            shop_name=validated_data.get('shop_name'),
            shop_description=validated_data.get('shop_description'),
            bank_account=validated_data.get('bank_account'),
            role='vendor'  # Set role to vendor
        )
        return user


class LogoutSerializer(serializers.Serializer):
    """
    Serializer for logout - adds token to blacklist
    """
    refresh = serializers.CharField(required=True)
