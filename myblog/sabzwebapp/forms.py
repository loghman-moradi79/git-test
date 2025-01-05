from cProfile import label

from django import forms
from .models import *


class TicketForm(forms.Form):
    SUBJECT_CHOICE = (
        ("پیشنهاد", "پیشنهاد"),
        ("انتقاد", "انتقاد"),
        ("گزارش", "گزارش"),
    )

    message = forms.CharField(widget=forms.Textarea, required=True)
    name = forms.CharField(max_length=20, required=True)
    email = forms.EmailField(max_length=50)
    phone = forms.CharField(max_length=11, required=True)
    subject = forms.ChoiceField(choices=SUBJECT_CHOICE, required=True)

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if not phone.isnumeric():
            raise forms.ValidationError("شماره تلفن عددی نیست")
        else:
            return phone


class CommentForm(forms.ModelForm):
    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) < 3:
            raise forms.ValidationError('طول نام کمتر از 3 کاراکتر میباشد!')
        else:
            return name

    class Meta:
        model = Comment
        fields = ['name', 'body']


class PostForm(forms.ModelForm):
    image_1 = forms.ImageField(label="تصویر اول ")
    image_2 = forms.ImageField(label="تصویر دوم ")

    class Meta:
        model = Post
        fields = ['title', 'description', 'category', 'reading_time']


class SearchForm(forms.Form):
    query = forms.CharField()


class RegisterForm(forms.ModelForm):
    password = forms.CharField(max_length=20, widget=forms.PasswordInput, label="رمز عبور")
    repeat_password = forms.CharField(max_length=20, widget=forms.PasswordInput, label="تکرار رمز عبور")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        repeat_password = cleaned_data.get('repeat_password')

        if repeat_password != password:
            raise forms.ValidationError('رمز عبور و تکرار آن باهم مطابقت ندارند')
        return cleaned_data


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class AccountEditForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['date_of_birth', 'bio', 'job', 'photo']












