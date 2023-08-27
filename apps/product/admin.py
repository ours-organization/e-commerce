from django.contrib import admin
from .models import Products,Product_Image,Color,Category,Savat,Buy_History
# Register your models here.


admin.site.register(Products)
admin.site.register(Product_Image)
admin.site.register(Color)
admin.site.register(Category)
admin.site.register(Savat)
admin.site.register(Buy_History)