from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from apps.users.models import User
from django.shortcuts import render, get_object_or_404,get_list_or_404



class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Products(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200)
    price = models.IntegerField()
    info = models.TextField()
    like = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def get_image(self):
        image = Product_Image.objects.filter(color=self.pk)
        return image

    def get_images(self,id):
        image = get_list_or_404(Product_Image, color=id)
        return image


class Product_Size(models.Model):
    size = models.CharField(max_length=10)


class Color(models.Model):
    # product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='color')
    color = models.CharField(max_length=30)

    def __str__(self):
        return self.color


class Product_Image(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='productimage')
    color = models.ForeignKey(Color, on_delete=models.CASCADE, related_name="imagecolor")
    image = models.ImageField(upload_to='images/')
    size = models.CharField(max_length=10)
    is_default = models.BooleanField(default=False)
    
    def __str__(self):
        return self.product.name


    def get_image(self, id):
        if self.color==id:
            return self.image


class Savat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_savat')
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='product')


class Buy_History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_buy_history')
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='user_buy_product')
    price = models.IntegerField()
    stars = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    image_product_from_user = models.ImageField(upload_to='images/')
    buy_date = models.DateTimeField()