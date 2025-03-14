from django import forms
from .models import Post


class ContactForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ["title", "status", "category",'published_date']
