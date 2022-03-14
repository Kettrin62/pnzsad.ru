from django import forms

from .models import Order


class CartEditForm(forms.Form):
    quantity = forms.IntegerField(
        label='Кол-во:', max_value=100500, min_value=1
    )


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('first_name', 'last_name', 'phoneNumber', 'email')

    # def clean_email(self):
    #     name = self.cleaned_data['author_name']
    #     text = self.cleaned_data['text']
    #     if Comment.objects.filter(text=text, author_name=name).exclude():
    #         raise forms.ValidationError(
    #             'Вы уже оставляли такой отзыв! Просим вас не флудить!'
    #         )
    #     return text
