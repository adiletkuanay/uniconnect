from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('university_admin', 'University Administrator'),
        ('system_admin', 'System Administrator'),
    )

    email = models.EmailField(_('email address'), unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    phone_number = models.CharField(max_length=15, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)

    # Additional student-specific fields
    iin = models.CharField(max_length=12, blank=True, help_text="Individual Identification Number")
    current_school = models.CharField(max_length=200, blank=True)
    graduation_year = models.IntegerField(null=True, blank=True)
    gpa = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    
    # University admin specific fields
    university = models.ForeignKey(
        'universities.University',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='administrators'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
