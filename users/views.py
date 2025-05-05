from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from allauth.account.utils import perform_login
from django.contrib.auth import logout
from .forms import UserRegistrationForm, UserProfileForm
from applications.models import Application, Document
from django.db.models import Q
from django.http import JsonResponse
import os

# Create your views here.

def register(request):
    # Redirect logged-in users
    if request.user.is_authenticated:
        messages.info(request, 'You are already registered and logged in.')
        return redirect('dashboard:dashboard')
        
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Use allauth's perform_login to handle the login
            perform_login(
                request, user,
                email_verification='optional'  # You can change this to 'mandatory' if needed
            )
            messages.success(request, 'Registration successful! Welcome to UniConnect!')
            return redirect('dashboard:dashboard')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def profile(request):
    # Get user's applications with related documents
    applications = Application.objects.filter(
        applicant=request.user
    ).select_related(
        'program',
        'program__university'
    ).prefetch_related(
        'documents'
    ).order_by('-created_at')
    
    # Get all documents from all applications
    documents = Document.objects.filter(
        application__applicant=request.user
    ).select_related(
        'application',
        'application__program'
    ).order_by('-created_at')
    
    # Group documents by type
    document_types = {}
    for doc in documents:
        if doc.document_type not in document_types:
            document_types[doc.document_type] = doc
    
    context = {
        'user': request.user,
        'applications': applications,
        'document_types': document_types,
        'documents': documents,
    }
    
    return render(request, 'users/profile.html', context)

@login_required
def settings(request):
    return render(request, 'users/settings.html')

@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        # Logout before deleting
        logout(request)
        # Delete the user account
        user.delete()
        messages.success(request, 'Your account has been successfully deleted.')
        return redirect('home')
    return redirect('users:settings')

@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('users:profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'users/profile_edit.html', {'form': form})

@login_required
def upload_document(request):
    if request.method == 'POST':
        if 'document' in request.FILES:
            document = request.FILES['document']
            # Check file type
            allowed_types = ['application/pdf', 'application/msword', 
                           'application/vnd.openxmlformats-officedocument.wordprocessingml.document']
            
            if document.content_type in allowed_types:
                # Create document object
                Document.objects.create(
                    user=request.user,
                    file=document
                )
                messages.success(request, 'Document uploaded successfully.')
                return redirect('users:profile')
            else:
                messages.error(request, 'Invalid file type. Please upload PDF, DOC, or DOCX files only.')
        else:
            messages.error(request, 'Please select a document to upload.')
    
    return render(request, 'users/document_form.html')
