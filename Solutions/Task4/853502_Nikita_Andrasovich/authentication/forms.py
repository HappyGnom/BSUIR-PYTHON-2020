from django import forms

class RegisterForm (forms.Form):
    user_email = forms.EmailField(max_length=30, label='', widget=forms.EmailInput(
        attrs={'class': 'text-input', 'placeholder': 'Your email'}))

    first_name = forms.CharField(max_length=30, label='', widget=forms.TextInput(
        attrs={'class': 'text-input', 'placeholder': 'Your first name'}))

    second_name = forms.CharField(max_length=30, label='', widget=forms.TextInput(
        attrs={'class': 'text-input', 'placeholder': 'Your second name'}))
    
    password = forms.CharField(max_length=30, label='', widget=forms.PasswordInput(
        attrs={'class': 'text-input', 'placeholder': 'Password'}))
