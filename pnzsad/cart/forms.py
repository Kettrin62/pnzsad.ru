from django import forms


class CartEditForm(forms.Form):
    quantity = forms.IntegerField(
        label='Кол-во:', max_value=100000, min_value=1
    )
