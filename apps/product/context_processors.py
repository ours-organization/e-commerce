from apps.product.models import Category


def header_date(request):
    category = Category.objects.all()
    date = {
        'categories':category
    }
    return date