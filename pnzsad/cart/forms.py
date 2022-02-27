from django import forms

from .models import Order


class CartEditForm(forms.Form):
    quantity = forms.IntegerField(
        label='Кол-во:', max_value=100000, min_value=1
    )


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('first_name', 'last_name', 'email')
