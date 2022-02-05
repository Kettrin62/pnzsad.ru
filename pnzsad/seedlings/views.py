from django.shortcuts import render, get_object_or_404

from .models import Category, Swiper, Seedling


def index(request):
    categoryes = Category.objects.all()
    swiper = Swiper.objects.all()

    return render(
        request,
        'seedlings/index.html',
        {
            'categoryes': categoryes,
            'swiper': swiper
        }
    )


def seedlings(request, category_slug=None):
    categoryes = Category.objects.all()

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        seedlings = Seedling.objects.filter(category=category, available=True)
        return render(
            request,
            'seedlings/test.html',
            {
                'categoryes': categoryes,
                'current_category': category,
                'seedlings': seedlings
            }
        )

    seedlings = Seedling.objects.filter(available=True)
    return render(
            request,
            'seedlings/test.html',
            {
                'categoryes': categoryes,
                'current_category': 'Все категории',
                'seedlings': seedlings
            }
        )
