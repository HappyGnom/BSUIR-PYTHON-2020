from django import forms


class ClientEmailForm (forms.Form):
    client_email = forms.EmailField(max_length=30, label='', widget=forms.EmailInput(
        attrs={'class': 'email-input', 'placeholder': 'Your email'}))


class LoginForm (forms.Form):
    user_email = forms.EmailField(max_length=30, label='', widget=forms.EmailInput(
        attrs={'class': 'log-input', 'placeholder': 'Login/email'}))

    password = forms.CharField(max_length=30, label='', widget=forms.PasswordInput(
        attrs={'class': 'log-input', 'placeholder': 'Password'}))
