from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render, redirect

from pnzsad.settings import COUNT_COMMENTS, COUNT_SEEDLINGS

from .forms import CommentForm
from .models import Category, Seedling, Swiper

PAGINATOR_CLASS = {
    'seedlings': 'seedlings',
    'seedling_page': 'seedling_page',
}


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
                'elements': cards,
                'paginator_class': PAGINATOR_CLASS['seedlings']
            }
        )


def seedling_page(request, category_slug, seedling_slug):
    category = get_object_or_404(Category, slug=category_slug)
    seedling = get_object_or_404(Seedling, slug=seedling_slug)

    author_name = ''
    if request.user.is_authenticated:
        author_name = request.user.first_name
    form = CommentForm(
        request.POST or None,
        initial={'author_name': author_name}
    )
    if form.is_valid():
        new_comment = form.save(commit=False)
        new_comment.seedling = seedling
        form.save()
        return redirect(
            request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found')
        )

    comments = seedling.comments.all()
    comments = get_paginator_page(request, comments, COUNT_COMMENTS)

    return render(
            request,
            'seedlings/seedling_page.html',
            {
                'current_category': category,
                'seedling': seedling,
                'elements': comments,
                'form': form,
                'paginator_class': PAGINATOR_CLASS['seedling_page']
            }
        )
