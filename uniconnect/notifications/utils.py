from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from notifications.models import Notification
from django.utils import timezone

def send_email_notification(subject, template_name, context, recipient_list):
    """
    Send an email notification using a template.
    """
    html_message = render_to_string(f'emails/{template_name}.html', context)
    plain_message = render_to_string(f'emails/{template_name}.txt', context)
    
    send_mail(
        subject=subject,
        message=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=recipient_list,
        html_message=html_message,
        fail_silently=False
    )

def create_in_app_notification(user, title, message, notification_type, related_object=None):
    """
    Create an in-app notification for a user.
    """
    notification = Notification.objects.create(
        user=user,
        title=title,
        message=message,
        notification_type=notification_type,
        related_object=related_object
    )
    return notification

def send_document_verification_notification(document):
    """
    Send notification when a document is verified.
    """
    subject = 'Document Verification Update'
    context = {
        'document': document,
        'student': document.student,
        'verification_status': document.status,
        'verification_notes': document.verification_notes
    }
    
    # Send email notification
    send_email_notification(
        subject=subject,
        template_name='document_verification',
        context=context,
        recipient_list=[document.student.email]
    )
    
    # Create in-app notification
    create_in_app_notification(
        user=document.student,
        title='Document Verification Update',
        message=f'Your {document.document_type} document has been {document.status}.',
        notification_type='document_verification',
        related_object=document
    )

def send_application_approval_notification(application):
    """
    Send notification when an application is approved.
    """
    subject = 'Application Status Update'
    context = {
        'application': application,
        'student': application.student,
        'program': application.program,
        'status': application.status,
        'review_notes': application.review_notes
    }
    
    # Send email notification
    send_email_notification(
        subject=subject,
        template_name='application_approval',
        context=context,
        recipient_list=[application.student.email]
    )
    
    # Create in-app notification
    create_in_app_notification(
        user=application.student,
        title='Application Approved',
        message=f'Your application for {application.program.title} has been approved!',
        notification_type='application_approval',
        related_object=application
    )

def send_application_rejection_notification(application):
    """
    Send notification when an application is rejected.
    """
    subject = 'Application Status Update'
    context = {
        'application': application,
        'student': application.student,
        'program': application.program,
        'status': application.status,
        'review_notes': application.review_notes
    }
    
    # Send email notification
    send_email_notification(
        subject=subject,
        template_name='application_rejection',
        context=context,
        recipient_list=[application.student.email]
    )
    
    # Create in-app notification
    create_in_app_notification(
        user=application.student,
        title='Application Update',
        message=f'Your application for {application.program.title} has been {application.status}.',
        notification_type='application_rejection',
        related_object=application
    )

def send_welcome_notification(user):
    """
    Send welcome notification to new users.
    """
    subject = 'Welcome to UniConnect'
    context = {
        'user': user
    }
    
    # Send email notification
    send_email_notification(
        subject=subject,
        template_name='welcome',
        context=context,
        recipient_list=[user.email]
    )
    
    # Create in-app notification
    create_in_app_notification(
        user=user,
        title='Welcome to UniConnect',
        message='Thank you for joining UniConnect! Start exploring programs and universities.',
        notification_type='welcome'
    )

def send_password_reset_notification(user, reset_link):
    """
    Send password reset notification.
    """
    subject = 'Password Reset Request'
    context = {
        'user': user,
        'reset_link': reset_link
    }
    
    # Send email notification
    send_email_notification(
        subject=subject,
        template_name='password_reset',
        context=context,
        recipient_list=[user.email]
    )

def send_newsletter_notification(users, subject, content):
    """
    Send newsletter to multiple users.
    """
    for user in users:
        context = {
            'user': user,
            'content': content
        }
        
        # Send email notification
        send_email_notification(
            subject=subject,
            template_name='newsletter',
            context=context,
            recipient_list=[user.email]
        )
        
        # Create in-app notification
        create_in_app_notification(
            user=user,
            title=subject,
            message=content,
            notification_type='newsletter'
        ) 