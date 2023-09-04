from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.views import View
from .models import Category, Products, Color, Product_Image, Savat, Product_Size


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
                rasmlar = color.image.filter(color=color)
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
    template_name = 'products/product-detail.html'

    def get(self, request, id, *args, **kwargs):
        product = Products.objects.get(pk=id)
        colors = Color.objects.filter(product=product)
        selected_color = request.GET.get('color', '')


        sizes = product.size.all()
        if selected_color:
            images = Product_Image.objects.all().filter(color=selected_color)
            selected_color = int(selected_color)
        else:
            images = Product_Image.objects.all().filter(color=product.id)


        context = {
            'product': product,
            'colors': colors,
            'selected_color': selected_color,
            'images': images,
            'sizes': sizes
        }

        return render(request, self.template_name, context)
    def post(self, request, id):
        radio_color = request.POST['color']
        # size = request.POST['size']
        print(request.POST)
        product = Products.objects.get(pk=id)
        colors = Color.objects.filter(product=product)
        selected_color = request.GET.get('color', '')

        sizes = product.size.all()
        return render(request, 'products/test2.html')


def AddToCart(request,id, color):
    if request.method == 'POST':
        size = request.POST['size']
        product = Products.objects.get(pk=id)

        razmer = Product_Size.objects.get(pk=size)
        rangi = Color.objects.get(pk=color)
        all = Savat.objects.create(
            user=request.user,
            product=product,
            color=rangi,
            size=razmer

        )
        all.save()
        print(f'color:{color}, size:{size}, product:{product}')
        return render(request, 'products/test2.html')