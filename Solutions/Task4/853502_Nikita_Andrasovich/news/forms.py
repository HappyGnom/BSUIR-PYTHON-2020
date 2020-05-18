from django import forms


class EditForm (forms.Form):
    title_field = forms.CharField(max_length=30, label='', widget=forms.TextInput(
        attrs={'class': 'text-input', 'placeholder': 'Title'}))

    content_field = forms.CharField(label='', widget=forms.Textarea(
        attrs={'class': 'text-input', 'placeholder': 'Content', 'rows': 50, 'cols': 20, 'style': 'height: 15vw;'}))
