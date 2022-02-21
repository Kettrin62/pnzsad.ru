from django.core.paginator import Paginator
from django.shortcuts import HttpResponse, get_object_or_404, render

from pnzsad.settings import COUNT_COMMENTS, COUNT_SEEDLINGS

from .models import Category, Comment, Seedling, Swiper


def get_paginator_page(request, objects, count):
    paginator = Paginator(objects, count)
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

    cards = get_paginator_page(request, seedlings, COUNT_SEEDLINGS)

    return render(
            request,
            'seedlings/seedling_cards.html',
            {
                'current_category': category,
                'elements': cards
            }
        )


def seedling_page(request, category_slug, seedling_slug):
    category = get_object_or_404(Category, slug=category_slug)
    seedling = get_object_or_404(Seedling, slug=seedling_slug)
    comments = seedling.comments.all()

    comments = get_paginator_page(request, comments, COUNT_COMMENTS)

    return render(
            request,
            'seedlings/seedling_page.html',
            {
                'current_category': category,
                'seedling': seedling,
                'elements': comments
            }
        )
