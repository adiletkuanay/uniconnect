from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from universities.models import University as UniversitiesUniversity
from .models import (
    Program, Semester, Course, Faculty, ProgramOutcome, Testimonial, Application, Document, Review, Message
)

class UniversityForm(forms.ModelForm):
    class Meta:
        model = UniversitiesUniversity
        fields = [
            'name', 'description', 'logo', 'website', 'address',
            'city', 'email', 'phone', 'established_year',
            'accreditation_info', 'ranking'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'accreditation_info': forms.Textarea(attrs={'rows': 3}),
            'address': forms.Textarea(attrs={'rows': 2}),
            'established_year': forms.NumberInput(),
        }

class ProgramForm(forms.ModelForm):
    class Meta:
        model = Program
        fields = [
            'title', 'university', 'degree_level', 'field_of_study',
            'duration', 'language', 'description', 'start_date',
            'application_start_date', 'application_deadline', 'min_gpa',
            'english_requirement', 'other_requirements', 'tuition_fee',
            'scholarship_available'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'other_requirements': forms.Textarea(attrs={'rows': 3}),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'application_start_date': forms.DateInput(attrs={'type': 'date'}),
            'application_deadline': forms.DateInput(attrs={'type': 'date'}),
        }

class SemesterForm(forms.ModelForm):
    class Meta:
        model = Semester
        fields = ['program', 'number', 'title', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['semester', 'code', 'name', 'description', 'credits', 'prerequisites']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class FacultyForm(forms.ModelForm):
    class Meta:
        model = Faculty
        fields = [
            'program', 'name', 'title', 'bio', 'email', 'photo',
            'research_interests', 'publications'
        ]
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
            'research_interests': forms.Textarea(attrs={'rows': 3}),
            'publications': forms.Textarea(attrs={'rows': 3}),
        }

class ProgramOutcomeForm(forms.ModelForm):
    class Meta:
        model = ProgramOutcome
        fields = ['program', 'description', 'category']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = [
            'program', 'student_name', 'graduation_year', 'content',
            'photo', 'current_position'
        ]
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4}),
        }

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = [
            'high_school_gpa', 'unt_score', 'english_proficiency_type',
            'english_proficiency_score', 'personal_statement', 'achievements',
            'extracurricular_activities', 'is_scholarship_requested',
            'is_dormitory_requested', 'notes'
        ]
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
            'high_school_gpa': forms.NumberInput(attrs={'step': '0.01', 'min': '0', 'max': '4'}),
            'unt_score': forms.NumberInput(attrs={'step': '0.01'}),
            'english_proficiency_score': forms.NumberInput(attrs={'step': '0.01'}),
            'personal_statement': forms.Textarea(attrs={'rows': 4}),
            'achievements': forms.Textarea(attrs={'rows': 3}),
            'extracurricular_activities': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_high_school_gpa(self):
        gpa = self.cleaned_data.get('high_school_gpa')
        if gpa is not None:
            if gpa < 0 or gpa > 4:
                raise forms.ValidationError("GPA must be between 0 and 4")
        return gpa

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['document_type', 'file']
        widgets = {
            'file': forms.FileInput(attrs={'accept': '.pdf,.doc,.docx,.jpg,.jpeg,.png'}),
        }

class DocumentVerificationForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['status', 'verification_notes']
        widgets = {
            'verification_notes': forms.Textarea(attrs={'rows': 3}),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['application', 'notes', 'status', 'admin_notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 4}),
            'admin_notes': forms.Textarea(attrs={'rows': 3}),
        }

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['recipient', 'subject', 'content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4}),
        }

class ContactCoordinatorForm(forms.Form):
    subject = forms.CharField(max_length=200, required=True)
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}), required=True)

class ProgramSearchForm(forms.Form):
    degree_level = forms.ChoiceField(
        choices=Program.DEGREE_LEVELS,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    field_of_study = forms.CharField(max_length=200, required=False)
    language = forms.ChoiceField(
        choices=Program.LANGUAGES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    min_gpa = forms.DecimalField(
        max_digits=3,
        decimal_places=2,
        required=False,
        validators=[MinValueValidator(0), MaxValueValidator(4)],
        widget=forms.NumberInput(attrs={'step': '0.01', 'min': '0', 'max': '4'})
    )
    scholarship_available = forms.BooleanField(required=False) 