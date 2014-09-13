from django import forms

class ShortURLForm(forms.Form):
    original_url = forms.URLField(label='URL you would like to shorten', required=True)
