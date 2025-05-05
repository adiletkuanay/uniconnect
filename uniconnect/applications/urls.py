from django.urls import path
from . import views

app_name = 'applications'

urlpatterns = [
    # Program URLs
    path('programs/', views.program_list, name='program_list'),
    path('programs/<int:pk>/', views.program_detail, name='program_detail'),
    path('programs/create/', views.program_create, name='program_create'),
    path('programs/<int:pk>/update/', views.program_update, name='program_update'),
    
    # Application URLs
    path('applications/', views.application_list, name='application_list'),
    path('applications/<int:pk>/', views.application_detail, name='application_detail'),
    path('applications/create/<int:program_pk>/', views.application_create, name='application_create'),
    path('applications/<int:pk>/update/', views.application_update, name='application_update'),
    path('applications/<int:pk>/submit/', views.application_submit, name='application_submit'),
    
    # Document URLs
    path('applications/<int:application_pk>/documents/upload/', views.document_upload, name='document_upload'),
    path('documents/<int:pk>/verify/', views.document_verify, name='document_verify'),
    
    # Review URLs
    path('applications/<int:pk>/review/', views.application_review, name='application_review'),
    
    # Message URLs
    path('messages/', views.message_list, name='message_list'),
    path('messages/<int:pk>/', views.message_detail, name='message_detail'),
    path('messages/send/', views.message_send, name='message_send'),
    
    # Contact URLs
    path('programs/<int:program_pk>/contact/', views.contact_coordinator, name='contact_coordinator'),
    
    # Testimonial URLs
    path('programs/<int:program_pk>/testimonials/create/', views.testimonial_create, name='testimonial_create'),
    path('testimonials/<int:pk>/approve/', views.testimonial_approve, name='testimonial_approve'),
] 