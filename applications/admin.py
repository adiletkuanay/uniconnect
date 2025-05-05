from django.contrib import admin
from .models import (
    University, Program, Semester, Course, Faculty,
    ProgramOutcome, Testimonial, Application, Document,
    Review, Notification, Message
)
from universities.models import University as UniversityModel

@admin.register(UniversityModel)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'email', 'established_year')
    list_filter = ('city', 'established_year')
    search_fields = ('name', 'city', 'email')
    readonly_fields = ('name', 'city')
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'logo', 'website')
        }),
        ('Contact Information', {
            'fields': ('address', 'city', 'email', 'phone')
        }),
        ('Additional Information', {
            'fields': ('established_year', 'accreditation_info', 'ranking')
        }),
    )

@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ('title', 'university', 'degree_level', 'language')
    list_filter = ('degree_level', 'language', 'university')
    search_fields = ('title', 'university__name', 'description')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('title', 'university', 'degree_level', 'field_of_study', 'description')
        }),
        ('Program Details', {
            'fields': ('duration', 'language', 'tuition_fee')
        }),
        ('Requirements', {
            'fields': ('min_gpa', 'english_requirement', 'other_requirements')
        }),
        ('Dates', {
            'fields': ('application_start_date', 'application_deadline', 'start_date')
        }),
        ('Additional Information', {
            'fields': ('scholarship_available',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ('program', 'number', 'title')
    search_fields = ('program__title', 'title')
    list_filter = ('program', 'number')
    ordering = ('program', 'number')

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'semester', 'credits')
    search_fields = ('code', 'name', 'semester__title')
    list_filter = ('semester__program', 'semester__number')
    filter_horizontal = ('prerequisites',)

@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'program', 'email')
    search_fields = ('name', 'title', 'program__title', 'email')
    list_filter = ('program',)

@admin.register(ProgramOutcome)
class ProgramOutcomeAdmin(admin.ModelAdmin):
    list_display = ('program', 'category', 'description')
    search_fields = ('program__title', 'category', 'description')
    list_filter = ('program', 'category')

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('student_name', 'program', 'graduation_year', 'approved', 'created_at')
    search_fields = ('student_name', 'program__title', 'content')
    list_filter = ('program', 'graduation_year', 'approved')
    readonly_fields = ('created_at',)

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('applicant', 'program', 'status', 'submission_date', 'created_at')
    search_fields = ('applicant__username', 'program__title', 'personal_statement')
    list_filter = ('status', 'program__university', 'program', 'is_scholarship_requested', 'is_dormitory_requested')
    readonly_fields = ('created_at', 'updated_at', 'submission_date')
    date_hierarchy = 'created_at'

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('application', 'document_type', 'status', 'verified_by', 'verified_at')
    search_fields = ('application__applicant__username', 'document_type', 'verification_notes')
    list_filter = ('document_type', 'status', 'verified_by')
    readonly_fields = ('created_at', 'updated_at', 'verified_at')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('application', 'reviewer', 'status', 'created_at')
    search_fields = ('application__applicant__username', 'notes', 'admin_notes')
    list_filter = ('status', 'reviewer')
    readonly_fields = ('created_at',)

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'title', 'is_read', 'created_at')
    search_fields = ('recipient__username', 'title', 'message')
    list_filter = ('is_read',)
    readonly_fields = ('created_at',)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'subject', 'is_read', 'created_at')
    search_fields = ('sender__username', 'recipient__username', 'subject', 'content')
    list_filter = ('is_read',)
    readonly_fields = ('created_at',)
