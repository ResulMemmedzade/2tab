from django import forms
from django.forms import inlineformset_factory
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from books.models import Book, BookImage


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = [
            'title',
            'author_name',
            'description',
            'price',
            'published_year',
            'condition',
            'genre',
            'language',
        ]

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Kitabın adı'
            }),

            'author_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Müəllifin adı'
            }),

            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Ətraflı məlumat...'
            }),

            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),

            'published_year': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Məsələn: 2020',
                'min': '1',
                'step': '1'
            }),

            'condition': forms.Select(attrs={
                'class': 'form-select'
            }),

            'genre': forms.Select(attrs={
                'class': 'form-select'
            }),

            'language': forms.Select(attrs={
                'class': 'form-select'
            }),
        }


BookImageFormSet = inlineformset_factory(
    Book,
    BookImage,
    fields=['image'],
    extra=3,
    max_num=3,
    validate_max=True,
    can_delete=True,
    widgets={
        'image': forms.ClearableFileInput(
            attrs={
                'class': 'form-control',
                'accept': 'image/*',
            }
        )
    }
)


User = get_user_model()

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Şifrənizi daxil edin'}))
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Şifrənizi təkrar daxil edin'}))

    class Meta:
        model = User
        fields = ['name', 'email']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Adınızı daxil edin'}),
            'email': forms.EmailInput(attrs={'placeholder': 'email@numune.az'}),
        }

    def clean_password(self):
        password = self.cleaned_data.get('password')
        validate_password(password)
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise ValidationError("Şifrələr uyğun gəlmir.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(label="Ad və ya Email", widget=forms.TextInput(attrs={'placeholder': 'email@numune.az və ya Ad'}))
    password = forms.CharField(label="Şifrə", widget=forms.PasswordInput(attrs={'placeholder': 'Şifrənizi daxil edin'}))