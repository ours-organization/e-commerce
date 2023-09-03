from .views import HomePageView, ProductSearchView, ProductDetailView, CategoryView
from django.urls import path

app_name='products'

urlpatterns = [
    path('home/', HomePageView.as_view(), name='indexPage'),
    # path('category/', CategoryView.as_view(), name='category'),
    path('category/<str:category_name>/', CategoryView.as_view(), name='category'),
    path('product/detail/<str:pk>/', ProductDetailView.as_view(), name='detailPage'),
]