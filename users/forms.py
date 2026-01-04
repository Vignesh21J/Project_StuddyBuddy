from django.contrib.auth import get_user_model
User = get_user_model()
from django.contrib.auth.forms import UserCreationForm

from django import forms
from django.contrib.auth.forms import AuthenticationForm


class RegisterUserForm(UserCreationForm):
    class Meta:
        model=User
        fields = ["username", "email", "password1", "password2"]
        labels = {
            "username": "Username",
            "email": "Email address",
        }
        widgets = {
            "username": forms.TextInput(attrs={
                "placeholder": "Enter your first_name and last_name"
            }),
            "email": forms.EmailInput(attrs={
                "placeholder": "Enter your email address"
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["password1"].widget.attrs["placeholder"] = "Enter password"
        self.fields["password2"].widget.attrs["placeholder"] = "Confirm password"

    def clean_email(self):
        email = self.cleaned_data.get('email')
        return email.strip().lower()
    

class LoginUserForm(AuthenticationForm):
    username = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            "placeholder": "Enter your email address"
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["password"].widget.attrs["placeholder"] = "Enter password"


class EditUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields = ['avatar', 'username', 'bio']