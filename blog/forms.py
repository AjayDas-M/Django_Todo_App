from django import forms
from django.contrib.auth.models import User
from .models import Blog, Profile

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

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone', 'profile_pic']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})