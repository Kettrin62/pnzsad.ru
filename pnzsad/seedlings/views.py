from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, HttpResponse

from .models import Category, Swiper, Seedling
from pnzsad.settings import COUNT_SEEDLINGS


def get_paginator_page(request, objects):
    paginator = Paginator(objects, COUNT_SEEDLINGS)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    return page


def index(request):
    swiper = Swiper.objects.filter(available=True).values('text', 'image')

    return render(
        request,
        'seedlings/index.html',
        {
            'swiper': swiper
        }
    )


def seedlings(request, category_slug=None):

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        seedlings = Seedling.objects.filter(
            category=category,
            available=True
            )
    else:
        category = 'Все категории'
        seedlings = Seedling.objects.filter(
            available=True
            )

    cards = get_paginator_page(request, seedlings)

    return render(
            request,
            'seedlings/seedling_cards.html',
            {
                'current_category': category,
                'cards': cards
            }
        )


def seedling_page(request, category_slug, seedling_slug):
    category = get_object_or_404(Category, slug=category_slug)
    seedling = get_object_or_404(Seedling, slug=seedling_slug)

    return render(
            request,
            'seedlings/seedling_page.html',
            {
                'current_category': category,
                'seedling': seedling
            }
        )
