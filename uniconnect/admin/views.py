from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from datetime import timedelta
from applications.models import Application, Document
from accounts.models import User
from universities.models import University, Program
from django.db.models import Count, Q
from django.contrib import messages
from django.urls import reverse

def is_admin(user):
    return user.is_staff or user.is_superuser

@login_required
@user_passes_test(is_admin)
def dashboard(request):
    # Get statistics
    total_users = User.objects.count()
    new_users_today = User.objects.filter(
        date_joined__date=timezone.now().date()
    ).count()
    
    active_applications = Application.objects.filter(
        status__in=['submitted', 'under_review']
    ).count()
    pending_reviews = Application.objects.filter(
        status='submitted'
    ).count()
    
    total_documents = Document.objects.count()
    pending_verification = Document.objects.filter(
        status='pending'
    ).count()
    
    total_universities = University.objects.count()
    active_programs = Program.objects.filter(
        is_active=True
    ).count()
    
    # Get recent activities
    recent_activities = []
    
    # Add recent applications
    recent_apps = Application.objects.order_by('-submitted_at')[:5]
    for app in recent_apps:
        recent_activities.append({
            'timestamp': app.submitted_at,
            'description': f'New application submitted by {app.student.get_full_name()} for {app.program.title}'
        })
    
    # Add recent document uploads
    recent_docs = Document.objects.order_by('-uploaded_at')[:5]
    for doc in recent_docs:
        recent_activities.append({
            'timestamp': doc.uploaded_at,
            'description': f'New document uploaded by {doc.student.get_full_name()}: {doc.document_type}'
        })
    
    # Sort activities by timestamp
    recent_activities.sort(key=lambda x: x['timestamp'], reverse=True)
    recent_activities = recent_activities[:10]  # Limit to 10 most recent
    
    # Get pending applications
    pending_applications = Application.objects.filter(
        status='submitted'
    ).order_by('-submitted_at')[:5]
    
    # Get pending documents
    pending_documents = Document.objects.filter(
        status='pending'
    ).order_by('-uploaded_at')[:5]
    
    # Get recent users
    recent_users = User.objects.order_by('-date_joined')[:5]
    
    context = {
        'total_users': total_users,
        'new_users_today': new_users_today,
        'active_applications': active_applications,
        'pending_reviews': pending_reviews,
        'total_documents': total_documents,
        'pending_verification': pending_verification,
        'total_universities': total_universities,
        'active_programs': active_programs,
        'recent_activities': recent_activities,
        'pending_applications': pending_applications,
        'pending_documents': pending_documents,
        'recent_users': recent_users,
    }
    
    return render(request, 'admin/dashboard.html', context)

@login_required
@user_passes_test(is_admin)
def user_list(request):
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'admin/user_list.html', {'users': users})

@login_required
@user_passes_test(is_admin)
def user_edit(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'User updated successfully.')
            return redirect('admin:user_list')
    else:
        form = UserEditForm(instance=user)
    return render(request, 'admin/user_edit.html', {'form': form, 'user': user})

@login_required
@user_passes_test(is_admin)
def application_list(request):
    applications = Application.objects.all().order_by('-submitted_at')
    return render(request, 'admin/application_list.html', {'applications': applications})

@login_required
@user_passes_test(is_admin)
def document_list(request):
    documents = Document.objects.all().order_by('-uploaded_at')
    return render(request, 'admin/document_list.html', {'documents': documents})

@login_required
@user_passes_test(is_admin)
def document_verify(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    if request.method == 'POST':
        form = DocumentVerificationForm(request.POST, instance=document)
        if form.is_valid():
            document = form.save()
            if document.status == 'verified':
                # Send notification to student
                send_document_verification_notification(document)
            messages.success(request, 'Document verification status updated.')
            return redirect('admin:document_list')
    else:
        form = DocumentVerificationForm(instance=document)
    return render(request, 'admin/document_verify.html', {'form': form, 'document': document})

@login_required
@user_passes_test(is_admin)
def application_review(request, application_id):
    application = get_object_or_404(Application, id=application_id)
    if request.method == 'POST':
        form = ApplicationReviewForm(request.POST, instance=application)
        if form.is_valid():
            application = form.save()
            if application.status == 'approved':
                # Send acceptance notification
                send_application_approval_notification(application)
            elif application.status == 'rejected':
                # Send rejection notification
                send_application_rejection_notification(application)
            messages.success(request, 'Application review completed.')
            return redirect('admin:application_list')
    else:
        form = ApplicationReviewForm(instance=application)
    return render(request, 'admin/application_review.html', {'form': form, 'application': application}) 