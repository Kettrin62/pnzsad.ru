from django.views.generic.base import TemplateView

from .models import About


class ContactsView(TemplateView):
    template_name = 'about/contacts.html'


def about(request):
    markup = About.objects.filter(id=1).first()
    