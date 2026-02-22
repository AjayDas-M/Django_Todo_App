from django import forms
from .models import Blog

class BlogForm(forms.ModelForm):
    image = forms.ImageField(required=False)

    class Meta:
        model = Blog
        exclude = ('user', 'likes')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # This loop adds the Bootstrap class to every field automatically
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})