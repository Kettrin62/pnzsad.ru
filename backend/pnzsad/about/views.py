from django.shortcuts import render
from django.views.generic.base import TemplateView

from .models import About


class ContactsView(TemplateView):
    template_name = 'about/contacts.html'


def about(request):
    markup = About.objects.all().first()

    return render(
            request,
            'about/about.html',
            {
                'markup': markup.markup
            }
        )
