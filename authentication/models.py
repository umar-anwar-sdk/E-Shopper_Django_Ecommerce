from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.core.validators import EmailValidator
import re


class CustomUserManager(BaseUserManager):
    """Custom user manager for authentication"""
    
    def create_user(self, email, password=None, **extra_fields):
        """
        Create and save a regular user with the given email and password.
        """
        if not email:
            raise ValueError('Email is required')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and save a superuser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    """
    Custom User model with role-based authentication
    """
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('vendor', 'Vendor'),
        ('customer', 'Customer'),
    ]
    
    username = models.CharField(max_length=150, unique=False, null=True, blank=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    is_verified = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # For vendors
    shop_name = models.CharField(max_length=255, blank=True, null=True)
    shop_description = models.TextField(blank=True, null=True)
    bank_account = models.CharField(max_length=20, blank=True, null=True)
    brand_logo = models.ImageField(upload_to='vendors/logos/', blank=True, null=True)
    brand_banner = models.ImageField(upload_to='vendors/banners/', blank=True, null=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    objects = CustomUserManager()
    
    def __str__(self):
        return f"{self.email} ({self.get_role_display()})"
    
    def is_admin(self):
        return self.role == 'admin'
    
    def is_vendor(self):
        return self.role == 'vendor'
    
    def is_customer(self):
        return self.role == 'customer'
    
    class Meta:
        db_table = 'custom_user'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-created_at']


class TokenBlacklist(models.Model):
    """
    Model to store blacklisted JWT tokens for logout functionality
    """
    token = models.TextField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='blacklisted_tokens')
    blacklisted_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    
    class Meta:
        db_table = 'token_blacklist'
        verbose_name = 'Token Blacklist'
        verbose_name_plural = 'Token Blacklists'
    
    def __str__(self):
        return f"Token for {self.user.email} - Blacklisted at {self.blacklisted_at}"
