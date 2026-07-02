from django import forms
from django.contrib.auth.models import User
from .models import TestDriveRequest, Profile


class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        label="Parol",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Parol"})
    )
    password2 = forms.CharField(
        label="Parolni takror kiriting",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Parolni takror kiriting"})
    )

    class Meta:
        model = User
        fields = ["username", "email"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control", "placeholder": "F.I.SH. / Foydalanuvchi nomi"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Elektron manzil"}),
        }

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("password") != cleaned.get("password2"):
            raise forms.ValidationError("Parollar mos kelmadi!")
        return cleaned


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["avatar", "phone"]
        widgets = {
            "avatar": forms.FileInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "+998 90 123 45 67"}),
        }


class TestDriveForm(forms.ModelForm):
    class Meta:
        model = TestDriveRequest
        fields = ["full_name", "phone", "car", "message"]
        widgets = {
            "full_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "F.I.SH."}),
            "phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "+998 90 123 45 67"}),
            "car": forms.Select(attrs={"class": "form-control"}),
            "message": forms.Textarea(attrs={"class": "form-control", "placeholder": "Xabar (ixtiyoriy)", "rows": 3}),
        }
