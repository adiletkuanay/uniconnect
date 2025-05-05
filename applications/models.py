from django.db import models
from django.conf import settings
from universities.models import University
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

class Program(models.Model):
    DEGREE_LEVELS = [
        ('bachelor', 'Bachelor'),
        ('master', 'Master'),
        ('phd', 'PhD'),
        ('diploma', 'Diploma'),
        ('certificate', 'Certificate'),
    ]

    LANGUAGES = [
        ('en', 'English'),
        ('tr', 'Turkish'),
        ('ru', 'Russian'),
        ('fr', 'French'),
        ('de', 'German'),
    ]

    title = models.CharField(max_length=200)
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='programs')
    degree_level = models.CharField(max_length=20, choices=DEGREE_LEVELS)
    field_of_study = models.CharField(max_length=200)
    duration = models.IntegerField(help_text="Duration in months")
    language = models.CharField(max_length=10, choices=LANGUAGES)
    description = models.TextField()
    start_date = models.DateField()
    application_start_date = models.DateField()
    application_deadline = models.DateField()
    min_gpa = models.DecimalField(max_digits=3, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(4)])
    english_requirement = models.CharField(max_length=200)
    other_requirements = models.TextField(blank=True)
    tuition_fee = models.DecimalField(max_digits=10, decimal_places=2)
    scholarship_available = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.university.name}"

class Semester(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='curriculum')
    number = models.IntegerField()
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['number']

    def __str__(self):
        return f"Semester {self.number} - {self.program.title}"

class Course(models.Model):
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='courses')
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=200)
    description = models.TextField()
    credits = models.IntegerField()
    prerequisites = models.ManyToManyField('self', symmetrical=False, blank=True)

    def __str__(self):
        return f"{self.code} - {self.name}"

class Faculty(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='faculty')
    name = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    bio = models.TextField()
    email = models.EmailField()
    photo = models.ImageField(upload_to='faculty_photos/', null=True, blank=True)
    research_interests = models.TextField(blank=True)
    publications = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} - {self.program.title}"

class ProgramOutcome(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='outcomes')
    description = models.TextField()
    category = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.category} - {self.program.title}"

class Testimonial(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='testimonials')
    student_name = models.CharField(max_length=200)
    graduation_year = models.IntegerField()
    content = models.TextField()
    photo = models.ImageField(upload_to='testimonial_photos/', null=True, blank=True)
    current_position = models.CharField(max_length=200, blank=True)
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student_name} - {self.program.title}"

class Application(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('needs_revision', 'Needs Revision'),
    ]

    ENGLISH_PROFICIENCY_TYPES = [
        ('ielts', 'IELTS'),
        ('toefl', 'TOEFL'),
        ('duolingo', 'Duolingo'),
        ('other', 'Other'),
    ]

    applicant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='applications')
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='applications')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    submission_date = models.DateTimeField(null=True, blank=True)
    
    # Academic Information
    high_school_gpa = models.DecimalField(max_digits=3, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(4)])
    unt_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    english_proficiency_type = models.CharField(max_length=20, choices=ENGLISH_PROFICIENCY_TYPES, null=True, blank=True)
    english_proficiency_score = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    
    # Additional Information
    personal_statement = models.TextField()
    achievements = models.TextField(blank=True)
    extracurricular_activities = models.TextField(blank=True)
    
    # Additional Requests
    is_scholarship_requested = models.BooleanField(default=False)
    is_dormitory_requested = models.BooleanField(default=False)
    
    # Notes
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.applicant.username}'s application for {self.program.title}"

class Document(models.Model):
    DOCUMENT_TYPES = [
        ('transcript', 'Transcript'),
        ('diploma', 'Diploma'),
        ('passport', 'Passport'),
        ('photo', 'Photo'),
        ('cv', 'CV'),
        ('motivation_letter', 'Motivation Letter'),
        ('recommendation_letter', 'Recommendation Letter'),
        ('english_proficiency', 'English Proficiency Certificate'),
        ('other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('verified', 'Verified'),
        ('rejected', 'Rejected'),
    ]

    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=50, choices=DOCUMENT_TYPES)
    file = models.FileField(upload_to='application_documents/')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    verification_notes = models.TextField(blank=True)
    verified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='verified_documents')
    verified_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_document_type_display()} - {self.application}"

class Review(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    notes = models.TextField()
    status = models.CharField(max_length=20, choices=Application.STATUS_CHOICES)
    admin_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.reviewer.username} for {self.application}"

class Notification(models.Model):
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.recipient.username}"

class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_messages')
    subject = models.CharField(max_length=200)
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject} - {self.sender.username} to {self.recipient.username}"
