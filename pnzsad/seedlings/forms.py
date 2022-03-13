from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('author_name', 'text',)

    def clean_text(self):
        name = self.cleaned_data['author_name']
        text = self.cleaned_data['text']
        if Comment.objects.filter(text=text, author_name=name).exclude():
            raise forms.ValidationError(
                'Вы уже оставляли такой комментарий! Просим вас не флудить!'
            )
        return text
