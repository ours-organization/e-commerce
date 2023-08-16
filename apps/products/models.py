from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from apps.users.models import User
# Create your models here.

class Products(models.Model):
    product_name = models.CharField(max_length=200)
    product_title = models.TextField()
    product_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.IntegerField()
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    size = models.CharField(max_length=10)
    product_info = models.TextField()
    like = models.BooleanField(default=False)


class Category(models.Model):
    category_name = models.CharField(max_length=50)

class Product_Image(models.Model):
    image = models.ImageField()

class Color(models.Model):
    color = models.CharField(max_length=30)
    color_image = models.ForeignKey(Product_Image, on_delete=models.CASCADE)

class Savat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)

class Buy_History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    price = models.IntegerField()
    stars = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    image_product_from_user = models.ImageField()
    buy_date = models.DateTimeField()