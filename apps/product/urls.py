from .views import HomePageView, ProductSearchView, ProductDetailView
from django.urls import path
app_name='products'
urlpatterns = [
    path('home/', HomePageView.as_view(), name='indexPage'),
    path('category/<int:category>/', ProductSearchView.as_view(), name='category'),
    path('product/detail/<int:id>/', ProductDetailView.as_view(), name='detailPage'),
]