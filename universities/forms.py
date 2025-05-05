from django import forms
from .models import University

class UniversityForm(forms.ModelForm):
    class Meta:
        model = University
        fields = [
            'name', 'description', 'logo', 'document', 'website', 'address', 
            'city', 'email', 'phone', 'established_year', 
            'accreditation_info', 'ranking'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'address': forms.Textarea(attrs={'rows': 3}),
            'accreditation_info': forms.Textarea(attrs={'rows': 4}),
        } 