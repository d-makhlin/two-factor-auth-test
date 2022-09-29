from django import forms
from django.contrib.auth.forms import UserCreationForm

from users.models.user import User


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    phone_no = forms.CharField(max_length=20)
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)
    use_two_step_auth = forms.BooleanField()

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "phone_no",
            "password1",
            "password2",
            "use_two_step_auth",
        ]
