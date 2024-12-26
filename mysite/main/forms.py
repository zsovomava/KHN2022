from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']


class VideochatCodeForm(forms.Form):
    code = forms.CharField(max_length=50, label='Megbeszéléskód')
