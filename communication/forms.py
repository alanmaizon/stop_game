from django import forms
from .models import WordSubmission

class WordSubmissionForm(forms.ModelForm):
    class Meta:
        model = WordSubmission
        fields = ['category', 'word']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'word': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter a word'}),
        }
