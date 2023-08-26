from django.contrib import admin
from .models import Products,Product_Image,Color,Category,Savat,Buy_History, Product_Size
# Register your models here.


class ProductImageInline(admin.TabularInline):
    model = Product_Image
\

class ProductAmin(admin.ModelAdmin):
    inlines = [ProductImageInline]


admin.site.register(Products, ProductAmin)
admin.site.register(Product_Image)
admin.site.register(Color)
admin.site.register(Category)
admin.site.register(Savat)
admin.site.register(Buy_History)