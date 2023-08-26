from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.views import View
from .models import Category, Products, Color, Product_Image


# Create your views here.
class HomePageView(View):
    def get(self,request):
        products = Products.objects.all()
        context = {
            'products': products,
        }
        return render(request, 'base.html', context)

class ProductSearchView(View):
    def get(self, request, category):
        id = Category.objects.get(pk=category)
        products = Products.objects.filter(category=id)
        images = []
        for product in products:
            colors = product.color.filter(product=product)
            for color in colors:
                rasmlar = color.imagecolor.filter(color=color)
                for rasm in rasmlar:
                    print(rasm)
                    images.append(rasm)
        # for product in products:
        #     img = product.get_image()
        #     images.append(img)

        context ={
            'products':products,
            'images':images,
        }

        return render(request, 'products/search-result.html', context)

class ProductDetailView(View):
    def get(self, request, id):
        product = get_object_or_404(Products, pk=id)
        colors = Color.objects.filter(product=product)
        selected_color = request.GET.get('color')

        if selected_color:
            color_images = Product_Image.objects.filter(color__color=selected_color)
        else:
            color_images = Product_Image.objects.filter(color__product=product).first()

        context = {
            'product': product,
            'colors': colors,
            'color_images': color_images,
            'selected_color': selected_color,
        }
        return render(request, 'products/product-detail.html', context)
        # search_query = request.GET.get('q', '')
        # page_size = request.GET.get('page_size', 2)
        #
        # products = get_list_or_404(Products, pk=id)
        # images = []
        # rang = []
        # for product in products:
        #     colors = product.color.all()
        #     rang.append(colors)
        #     print(colors)
        #     for color in colors:
        #         rasmlar = color.image.filter(color=color)
        #         for rasm in rasmlar:
        #             print(rasm)
        #             images.append(rasm)
        #
        # for color in rang:
        #     print(color)
        # context = {
        #     'products': products,
        #     'colors': rang,
        #     'images':images
        # }
        # paginator = Paginator(context, page_size)
        # print(context)
        # page_num = request.GET.get('page', 1)
        # page_obj = paginator.get_page(page_num)
        # return render(
        #     request,
        #     "books/list.html",
        #     {"page_obj": page_obj,
        #      }
        # )
        # # return render(request, 'products/product-detail.html', context)
    def post(self, request):
        pass


