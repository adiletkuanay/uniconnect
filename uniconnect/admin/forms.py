from django import forms
from accounts.models import User
from applications.models import Application, Document
from django.contrib.auth.forms import UserChangeForm

class UserEditForm(UserChangeForm):
    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name', 'last_name',
            'is_active', 'is_staff', 'is_superuser'
        ]
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class DocumentVerificationForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['status', 'verification_notes']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'verification_notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter verification notes here...'
            })
        }

class ApplicationReviewForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['status', 'review_notes', 'admin_notes']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'review_notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter review notes here...'
            }),
            'admin_notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter admin notes here...'
            })
        }

class UniversityAddForm(forms.ModelForm):
    class Meta:
        model = University
        fields = [
            'name', 'country', 'city', 'description',
            'website', 'email', 'phone', 'address',
            'logo', 'type', 'founded_year', 'rank',
            'acceptance_rate', 'student_staff_ratio'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.Select(attrs={'class': 'form-select'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'type': forms.Select(attrs={'class': 'form-select'}),
            'founded_year': forms.NumberInput(attrs={'class': 'form-control'}),
            'rank': forms.NumberInput(attrs={'class': 'form-control'}),
            'acceptance_rate': forms.NumberInput(attrs={'class': 'form-control'}),
            'student_staff_ratio': forms.TextInput(attrs={'class': 'form-control'})
        }

class ProgramAddForm(forms.ModelForm):
    class Meta:
        model = Program
        fields = [
            'title', 'university', 'degree_level', 'field_of_study',
            'duration', 'language', 'start_date', 'application_deadline',
            'min_gpa', 'english_requirement', 'tuition_fee',
            'scholarship_available', 'description', 'curriculum'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'university': forms.Select(attrs={'class': 'form-select'}),
            'degree_level': forms.Select(attrs={'class': 'form-select'}),
            'field_of_study': forms.TextInput(attrs={'class': 'form-control'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control'}),
            'language': forms.Select(attrs={'class': 'form-select'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'application_deadline': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'min_gpa': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'english_requirement': forms.Select(attrs={'class': 'form-select'}),
            'tuition_fee': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'curriculum': forms.Textarea(attrs={'class': 'form-control', 'rows': 4})
        } 