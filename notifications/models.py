from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from accounts.models import User

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('document_verification', 'Document Verification'),
        ('application_approval', 'Application Approval'),
        ('application_rejection', 'Application Rejection'),
        ('welcome', 'Welcome'),
        ('password_reset', 'Password Reset'),
        ('newsletter', 'Newsletter'),
        ('system', 'System'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=255)
    message = models.TextField()
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPES)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Generic foreign key for related objects
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    related_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'is_read']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.title} - {self.user.get_full_name()}"

    def mark_as_read(self):
        self.is_read = True
        self.save()

    @classmethod
    def get_unread_count(cls, user):
        return cls.objects.filter(user=user, is_read=False).count()

    @classmethod
    def get_recent_notifications(cls, user, limit=10):
        return cls.objects.filter(user=user).order_by('-created_at')[:limit]

    @classmethod
    def mark_all_as_read(cls, user):
        cls.objects.filter(user=user, is_read=False).update(is_read=True) 