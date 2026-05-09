from django.contrib import admin

from home.models import Category, Sub_Category, Product, Contact_us, Order, Brand, Slider

# Register your models here.
admin.site.register(Category)
admin.site.register(Sub_Category)
admin.site.register(Product)
admin.site.register(Contact_us)
admin.site.register(Order)
admin.site.register(Brand)
admin.site.register(Slider)

