from django.db import models
from django.utils.translation import gettext_lazy as _

class University(models.Model):
    TYPE_CHOICES = (
        ('public', 'Public'),
        ('private', 'Private'),
        ('international', 'International'),
    )

    name = models.CharField(max_length=200)
    description = models.TextField()
    logo = models.ImageField(upload_to='university_logos/', null=True, blank=True)
    document = models.FileField(upload_to='university_documents/', null=True, blank=True)
    website = models.URLField()
    address = models.TextField()
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100, null=True, blank=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='public', null=True, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    established_year = models.IntegerField()
    accreditation_info = models.TextField()
    ranking = models.IntegerField(null=True, blank=True)
    students_count = models.IntegerField(default=0)
    
    class Meta:
        verbose_name = _('university')
        verbose_name_plural = _('universities')
        ordering = ['name']

    def __str__(self):
        return self.name
