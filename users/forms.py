from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    phone_number = forms.CharField(required=False, max_length=15)
    date_of_birth = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    role = forms.ChoiceField(
        choices=User.ROLE_CHOICES,
        initial='student',
        required=True
    )
    
    # Student specific fields
    iin = forms.CharField(
        max_length=12,
        required=False,
        help_text="Individual Identification Number"
    )
    current_school = forms.CharField(max_length=200, required=False)
    graduation_year = forms.IntegerField(required=False)
    gpa = forms.DecimalField(max_digits=3, decimal_places=2, required=False)

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name',
            'password1', 'password2', 'phone_number', 'date_of_birth',
            'role', 'iin', 'current_school', 'graduation_year', 'gpa'
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'autofocus': True})
        self.fields['username'].help_text = _('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.')
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.phone_number = self.cleaned_data.get('phone_number', '')
        user.date_of_birth = self.cleaned_data.get('date_of_birth')
        user.role = self.cleaned_data.get('role', 'student')
        user.iin = self.cleaned_data.get('iin', '')
        user.current_school = self.cleaned_data.get('current_school', '')
        user.graduation_year = self.cleaned_data.get('graduation_year')
        user.gpa = self.cleaned_data.get('gpa')
        
        if commit:
            user.save()
        return user

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'email', 'phone_number',
            'date_of_birth', 'profile_picture', 'bio',
            'current_school', 'graduation_year', 'gpa', 'iin'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'bio': forms.Textarea(attrs={'rows': 4}),
        } 