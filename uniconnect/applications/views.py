from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count, Avg
from django.utils import timezone
from .models import (
    University, Program, Application, Document, Review,
    Notification, Message, Testimonial
)
from .forms import (
    UniversityForm, ProgramForm, ApplicationForm, DocumentForm,
    DocumentVerificationForm, ReviewForm, MessageForm,
    ContactCoordinatorForm, ProgramSearchForm, TestimonialForm
)

def is_admin(user):
    return user.is_staff

def is_applicant(user):
    return not user.is_staff

# Program Views
def program_list(request):
    form = ProgramSearchForm(request.GET)
    programs = Program.objects.all()
    
    if form.is_valid():
        if form.cleaned_data.get('degree_level'):
            programs = programs.filter(degree_level=form.cleaned_data['degree_level'])
        if form.cleaned_data.get('field_of_study'):
            programs = programs.filter(field_of_study__icontains=form.cleaned_data['field_of_study'])
        if form.cleaned_data.get('language'):
            programs = programs.filter(language=form.cleaned_data['language'])
        if form.cleaned_data.get('min_gpa'):
            programs = programs.filter(min_gpa__lte=form.cleaned_data['min_gpa'])
        if form.cleaned_data.get('scholarship_available'):
            programs = programs.filter(scholarship_available=True)
    
    paginator = Paginator(programs, 10)
    page = request.GET.get('page')
    programs = paginator.get_page(page)
    
    return render(request, 'applications/program_list.html', {
        'programs': programs,
        'form': form
    })

def program_detail(request, pk):
    program = get_object_or_404(Program, pk=pk)
    similar_programs = Program.objects.filter(
        field_of_study=program.field_of_study
    ).exclude(pk=pk)[:5]
    
    return render(request, 'applications/program_detail.html', {
        'program': program,
        'similar_programs': similar_programs
    })

@user_passes_test(is_admin)
def program_create(request):
    if request.method == 'POST':
        form = ProgramForm(request.POST)
        if form.is_valid():
            program = form.save()
            messages.success(request, 'Program created successfully.')
            return redirect('program_detail', pk=program.pk)
    else:
        form = ProgramForm()
    
    return render(request, 'applications/program_form.html', {'form': form})

@user_passes_test(is_admin)
def program_update(request, pk):
    program = get_object_or_404(Program, pk=pk)
    if request.method == 'POST':
        form = ProgramForm(request.POST, instance=program)
        if form.is_valid():
            form.save()
            messages.success(request, 'Program updated successfully.')
            return redirect('program_detail', pk=program.pk)
    else:
        form = ProgramForm(instance=program)
    
    return render(request, 'applications/program_form.html', {'form': form})

# Application Views
@login_required
def application_list(request):
    applications = Application.objects.filter(applicant=request.user)
    return render(request, 'applications/application_list.html', {
        'applications': applications
    })

@login_required
def application_detail(request, pk):
    application = get_object_or_404(Application, pk=pk, applicant=request.user)
    return render(request, 'applications/application_detail.html', {
        'application': application
    })

@login_required
def application_create(request, program_pk):
    program = get_object_or_404(Program, pk=program_pk)
    
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.applicant = request.user
            application.program = program
            application.save()
            messages.success(request, 'Application created successfully.')
            return redirect('application_detail', pk=application.pk)
    else:
        form = ApplicationForm(initial={'program': program})
    
    return render(request, 'applications/application_form.html', {
        'form': form,
        'program': program
    })

@login_required
def application_update(request, pk):
    application = get_object_or_404(Application, pk=pk, applicant=request.user)
    
    if application.status != 'draft':
        messages.error(request, 'Only draft applications can be updated.')
        return redirect('application_detail', pk=application.pk)
    
    if request.method == 'POST':
        form = ApplicationForm(request.POST, instance=application)
        if form.is_valid():
            form.save()
            messages.success(request, 'Application updated successfully.')
            return redirect('application_detail', pk=application.pk)
    else:
        form = ApplicationForm(instance=application)
    
    return render(request, 'applications/application_form.html', {
        'form': form,
        'application': application
    })

@login_required
def application_submit(request, pk):
    application = get_object_or_404(Application, pk=pk, applicant=request.user)
    
    if application.status != 'draft':
        messages.error(request, 'Only draft applications can be submitted.')
        return redirect('application_detail', pk=application.pk)
    
    required_documents = ['transcript', 'diploma', 'passport', 'photo']
    submitted_documents = application.documents.values_list('document_type', flat=True)
    
    missing_documents = [doc for doc in required_documents if doc not in submitted_documents]
    
    if missing_documents:
        messages.error(request, f'Please upload the following required documents: {", ".join(missing_documents)}')
        return redirect('application_detail', pk=application.pk)
    
    application.status = 'submitted'
    application.submission_date = timezone.now()
    application.save()
    
    messages.success(request, 'Application submitted successfully.')
    return redirect('application_detail', pk=application.pk)

# Document Views
@login_required
def document_upload(request, application_pk):
    application = get_object_or_404(Application, pk=application_pk, applicant=request.user)
    
    if application.status != 'draft':
        messages.error(request, 'Documents can only be uploaded for draft applications.')
        return redirect('application_detail', pk=application.pk)
    
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.application = application
            document.save()
            messages.success(request, 'Document uploaded successfully.')
            return redirect('application_detail', pk=application.pk)
    else:
        form = DocumentForm(initial={'application': application})
    
    return render(request, 'applications/document_form.html', {
        'form': form,
        'application': application
    })

@user_passes_test(is_admin)
def document_verify(request, pk):
    document = get_object_or_404(Document, pk=pk)
    
    if request.method == 'POST':
        form = DocumentVerificationForm(request.POST, instance=document)
        if form.is_valid():
            document = form.save(commit=False)
            document.verified_by = request.user
            document.verified_at = timezone.now()
            document.save()
            
            if document.status == 'verified':
                messages.success(request, 'Document verified successfully.')
            else:
                messages.warning(request, 'Document verification rejected.')
            
            return redirect('application_review', pk=document.application.pk)
    else:
        form = DocumentVerificationForm(instance=document)
    
    return render(request, 'applications/document_verify.html', {
        'form': form,
        'document': document
    })

# Review Views
@user_passes_test(is_admin)
def application_review(request, pk):
    application = get_object_or_404(Application, pk=pk)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.application = application
            review.reviewer = request.user
            review.save()
            
            application.status = review.status
            application.save()
            
            messages.success(request, 'Review submitted successfully.')
            return redirect('application_review', pk=application.pk)
    else:
        form = ReviewForm(initial={'application': application})
    
    return render(request, 'applications/application_review.html', {
        'application': application,
        'form': form
    })

# Message Views
@login_required
def message_list(request):
    messages = Message.objects.filter(
        Q(sender=request.user) | Q(recipient=request.user)
    ).order_by('-created_at')
    return render(request, 'applications/message_list.html', {
        'messages': messages
    })

@login_required
def message_detail(request, pk):
    message = get_object_or_404(Message, pk=pk)
    if message.sender != request.user and message.recipient != request.user:
        messages.error(request, 'You do not have permission to view this message.')
        return redirect('message_list')
    
    if message.recipient == request.user and not message.is_read:
        message.is_read = True
        message.save()
    
    return render(request, 'applications/message_detail.html', {
        'message': message
    })

@login_required
def message_send(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()
            messages.success(request, 'Message sent successfully.')
            return redirect('message_detail', pk=message.pk)
    else:
        form = MessageForm()
    
    return render(request, 'applications/message_form.html', {'form': form})

# Contact Views
@login_required
def contact_coordinator(request, program_pk):
    program = get_object_or_404(Program, pk=program_pk)
    
    if request.method == 'POST':
        form = ContactCoordinatorForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            
            # Create a message to the program coordinator
            Message.objects.create(
                sender=request.user,
                recipient=program.university.contact_email,
                subject=f"[Program Inquiry] {subject}",
                content=message
            )
            
            messages.success(request, 'Message sent to program coordinator.')
            return redirect('program_detail', pk=program.pk)
    else:
        form = ContactCoordinatorForm()
    
    return render(request, 'applications/contact_coordinator.html', {
        'form': form,
        'program': program
    })

# Testimonial Views
@login_required
def testimonial_create(request, program_pk):
    program = get_object_or_404(Program, pk=program_pk)
    
    if request.method == 'POST':
        form = TestimonialForm(request.POST, request.FILES)
        if form.is_valid():
            testimonial = form.save(commit=False)
            testimonial.program = program
            testimonial.save()
            messages.success(request, 'Testimonial submitted successfully.')
            return redirect('program_detail', pk=program.pk)
    else:
        form = TestimonialForm(initial={'program': program})
    
    return render(request, 'applications/testimonial_form.html', {
        'form': form,
        'program': program
    })

@user_passes_test(is_admin)
def testimonial_approve(request, pk):
    testimonial = get_object_or_404(Testimonial, pk=pk)
    testimonial.approved = True
    testimonial.save()
    messages.success(request, 'Testimonial approved successfully.')
    return redirect('program_detail', pk=testimonial.program.pk)
