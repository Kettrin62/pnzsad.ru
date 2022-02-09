from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404

from .models import Category, Swiper, Seedling
from pnzsad.settings import COUNT_SEEDLINGS


def get_paginator_page(request, objects):
    paginator = Paginator(objects, COUNT_SEEDLINGS)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    return page


def index(request):
    categoryes = Category.objects.all()
    swiper = Swiper.objects.filter(available=True).values('text', 'image')

    return render(
        request,
        'seedlings/index.html',
        {
            'categoryes': categoryes,
            'swiper': swiper
        }
    )


def seedlings(request, category_slug=None):
    categoryes = Category.objects.all().values('title', 'image')

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        seedlings = Seedling.objects.filter(
            category=category,
            available=True
            ).values(
            'title', 'image', 'short_description', 'retail_price',
            'wholesale_price', 'stock'
        )
        page = get_paginator_page(request, seedlings)
        return render(
            request,
            'seedlings/seedling_cards.html',
            {
                'categoryes': categoryes,
                'current_category': category,
                'page': page
            }
        )

    seedlings = Seedling.objects.filter(
        available=True
        ).values(
            'title', 'image', 'short_description', 'retail_price',
            'wholesale_price', 'stock'
    )
    return render(
            request,
            'seedlings/seedling_cards.html',
            {
                'categoryes': categoryes,
                'current_category': 'Все категории',
                'seedlings': seedlings
            }
        )
