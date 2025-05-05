from django.db import models
from django.utils.translation import gettext_lazy as _

class University(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    logo = models.ImageField(upload_to='university_logos/', null=True, blank=True)
    website = models.URLField()
    address = models.TextField()
    city = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    established_year = models.IntegerField()
    accreditation_info = models.TextField()
    ranking = models.IntegerField(null=True, blank=True)
    
    class Meta:
        verbose_name = _('university')
        verbose_name_plural = _('universities')
        ordering = ['name']

    def __str__(self):
        return self.name

class Program(models.Model):
    DEGREE_CHOICES = (
        ('bachelor', 'Bachelor'),
        ('master', 'Master'),
        ('phd', 'PhD'),
    )
    
    LANGUAGE_CHOICES = (
        ('kazakh', 'Kazakh'),
        ('russian', 'Russian'),
        ('english', 'English'),
    )

    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='programs')
    name = models.CharField(max_length=200)
    degree = models.CharField(max_length=20, choices=DEGREE_CHOICES)
    description = models.TextField()
    duration_years = models.DecimalField(max_digits=3, decimal_places=1)
    tuition_fee_per_year = models.DecimalField(max_digits=10, decimal_places=2)
    language_of_instruction = models.CharField(max_length=20, choices=LANGUAGE_CHOICES)
    credits_required = models.IntegerField()
    admission_requirements = models.TextField()
    application_deadline = models.DateField()
    start_date = models.DateField()
    scholarships_available = models.BooleanField(default=False)
    has_dormitory = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = _('program')
        verbose_name_plural = _('programs')
        ordering = ['university', 'name']

    def __str__(self):
        return f"{self.name} at {self.university.name}"
