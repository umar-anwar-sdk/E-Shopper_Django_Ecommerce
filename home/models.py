import datetime

from django.db import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class Category(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Sub_Category(models.Model):
    name = models.CharField(max_length=150)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Product(models.Model):
    Availability = (('In Stock', 'In Stock'), ('Out of Stock', 'Out of Stock'))
    Condition = (('New','New'), ('Used', 'Used'))

    Category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, default=True)
    sub_category = models.ForeignKey(Sub_Category, on_delete=models.CASCADE, null=True, default=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True, default=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    name = models.CharField(max_length=100)
    details = models.TextField(null=True)
    price = models.IntegerField()
    Availability = models.CharField(choices=Availability, null=True, max_length=100)
    Condition = models.CharField(choices=Condition, null=True, max_length=100)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email', error_messages={'exists': 'This Already Exists'})

    class Meta:
        model = User
        fields = {'username', 'email', 'password1', 'password2'}

    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError(self.fields['email'].error_message['exists'])
        return self.cleaned_data['email']


# contact us

class Contact_us(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    subject = models.CharField(max_length=100)
    message = models.TextField()

    def __str__(self):
        return self.email


class Order(models.Model):
    image = models.ImageField(upload_to='order/image', blank=True, null=True)
    product = models.CharField(max_length=1000, default='')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.CharField(max_length=5)
    price = models.IntegerField()
    address = models.TextField()
    phone = models.CharField(max_length=10)
    pincode = models.CharField(max_length=10)
    total = models.CharField(max_length=1000, default='')
    date = models.DateField(default=datetime.datetime.today)

    def __str__(self):
        return self.product



class Slider(models.Model):
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    price_img = models.ImageField(upload_to='images/', blank=True, null=True)
    title = models.CharField(max_length=255)
    sub_title = models.CharField(max_length=255)
    description = models.TextField(null=True)

    def __str__(self):
        return self.title