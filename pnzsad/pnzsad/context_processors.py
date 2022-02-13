import datetime as dt

from seedlings.models import Category

def get_year(request):
    year = dt.date.today().year
    return {'year': year}


def get_categories(request):
    categories = Category.objects.all()
    return {'categories': categories}