from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.views import View
from .models import Category, Products, Color, Product_Image

def for_all_pages(request):
    categories = Category.objects.all()
    return {'categories': categories}


class HomePageView(View):
    def get(self,request):
        products = Products.objects.all()
        context = {
            'products': products,
        }
        return render(request, 'products/index.html', context)


class CategoryView(View):
    def get(self, request, category_name):
        category =get_object_or_404(Category, name=category_name)
        products = Products.objects.filter(category=category)

        filtr = self.request.GET.get('filtr', None)
        if filtr:
            products = products.filter(product_name__icontains=filtr)
        return render(request, 'products/category.html', {'category': category, 'products': products})

    def post(self, request):
        return render(request, 'products/category.html', {})


        #   agar keraksiz kod deb xisoblasez o'ziz o'chirvorasz aka)

# class ProductSearchView(View):
#     def get(self, request, category):
#         id = Category.objects.get(pk=category)
#         products = Products.objects.filter(category=id)
#         images = []
#         for product in products:
#             colors = product.color.filter(product=product)
#             for color in colors:
#                 rasmlar = color.imagecolor.filter(color=color)
#                 for rasm in rasmlar:
#                     print(rasm)
#                     images.append(rasm)
#         # for product in products:
#         #     img = product.get_image()
#         #     images.append(img)

#         context = {
#             'products':products,
#             'images':images,
#         }

#         return render(request, 'products/search-result.html', context)
    

class ProductDetailView(View):
    def get(self, request, pk):
        product = Products.objects.get(id=pk)

        return render(request, 'products/test.html', {'product': product})


# class ProductDetailView(View):
#     template_name = 'products/test.html'

#     def get(self, request, id, *args, **kwargs):
#         product = Products.objects.get(pk=id)
#         colors = Color.objects.filter(product=product)
#         selected_color = request.GET.get('color', colors.first())

#         images = Product_Image.objects.all().filter(color=selected_color)
#         print(images)
#         context = {
#             'product': product,
#             'colors': colors,
#             'selected_color': selected_color,
#             'images': images,
#         }
#         return render(request, self.template_name, context)

# def product_detail(request, id):
#     product = Products.objects.get(pk=id)
#     colors = Color.objects.filter(product=product)
#     selected_color = request.GET.get('color', colors.first())
#
#     images = Product_Image.objects.filter(color=selected_color)
#
#     context = {
#         'product': product,
#         'colors': colors,
#         'selected_color': selected_color,
#         'images': images,
#     }
#     return render(request, 'products/product-detail.html', context)
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
    # def post(self, request):
    #     pass


