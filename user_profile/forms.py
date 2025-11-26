from django import forms
from .models import UserProfile
from Blogs.models import Blog

# ---------------- User Profile Form ----------------
class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ['phone', 'bio', 'profile_image', 'address']

    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)

        # User fields initial value
        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email

    def save(self, commit=True):
        profile = super(UserProfileForm, self).save(commit=False)

        # Update User model data
        user = profile.user
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.email = self.cleaned_data.get('email')

        if commit:
            user.save()
            profile.save()
        return profile


# ---------------- Blog Edit Form ----------------
class BlogEditForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'category', 'photo', 'content']
