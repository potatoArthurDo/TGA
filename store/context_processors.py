from .models import Category


# help categories show up on all pages
def categories_processcor(request):
    categories = Category.objects.all()
    return {'categories': categories}