from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count, Avg
from django.utils import timezone
from .models import (
    Program, Application, Document, Review,
    Notification, Message, Testimonial
)
from universities.models import University
from .forms import (
    ProgramForm, ApplicationForm, DocumentForm,
    DocumentVerificationForm, ReviewForm, MessageForm,
    ContactCoordinatorForm, ProgramSearchForm, TestimonialForm
)
from django import forms

def is_admin(user):
    return user.is_staff

def is_applicant(user):
    return not user.is_staff

# Program Views
def program_list(request):
    form = ProgramSearchForm(request.GET)
    programs = Program.objects.all()
    
    # Handle search query
    search_query = request.GET.get('search')
    if search_query:
        programs = programs.filter(
            Q(title__icontains=search_query) |
            Q(field_of_study__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(university__name__icontains=search_query)
        )
    
    # Handle form filters
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
    
    # Get unique values for filters
    universities = University.objects.all()
    degree_levels = Program.DEGREE_LEVELS
    languages = Program.LANGUAGES
    
    paginator = Paginator(programs, 10)
    page = request.GET.get('page')
    programs = paginator.get_page(page)
    
    return render(request, 'applications/program_list.html', {
        'programs': programs,
        'form': form,
        'universities': universities,
        'degree_levels': degree_levels,
        'languages': languages,
        'search_query': search_query
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

@login_required
def program_create(request):
    if not request.user.role in ['university_admin', 'system_admin']:
        messages.error(request, 'You do not have permission to create programs.')
        return redirect('dashboard:dashboard')

    if request.method == 'POST':
        form = ProgramForm(request.POST)
        if form.is_valid():
            program = form.save(commit=False)
            # If user is university admin, set their university
            if request.user.role == 'university_admin':
                program.university = request.user.university
            program.save()
            messages.success(request, 'Program created successfully.')
            return redirect('applications:program_detail', pk=program.pk)
        else:
            # Add form error messages
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'Error in {field}: {error}')
    else:
        initial = {}
        # If user is university admin, pre-set their university
        if request.user.role == 'university_admin':
            if not request.user.university:
                messages.error(request, 'You need to be assigned to a university before creating programs.')
                return redirect('dashboard:dashboard')
            initial['university'] = request.user.university
            form = ProgramForm(initial=initial)
            # Hide the university field
            form.fields['university'].widget = forms.HiddenInput()
        else:
            form = ProgramForm(initial=initial)
    
    # Add debug information to the template context
    context = {
        'form': form,
        'debug_info': {
            'user_role': request.user.role,
            'is_post': request.method == 'POST',
            'form_data': request.POST if request.method == 'POST' else None,
        }
    }
    return render(request, 'applications/program_form.html', context)

@login_required
def program_update(request, pk):
    program = get_object_or_404(Program, pk=pk)
    
    # Check if user has permission to update this program
    if not (request.user.role == 'system_admin' or 
            (request.user.role == 'university_admin' and request.user.university == program.university)):
        messages.error(request, 'You do not have permission to update this program.')
        return redirect('dashboard:dashboard')
    
    if request.method == 'POST':
        form = ProgramForm(request.POST, instance=program)
        if form.is_valid():
            form.save()
            messages.success(request, 'Program updated successfully.')
            return redirect('applications:program_detail', pk=program.pk)
        else:
            # Add form error messages
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'Error in {field}: {error}')
    else:
        form = ProgramForm(instance=program)
        # If user is university admin, hide the university field
        if request.user.role == 'university_admin':
            form.fields['university'].widget = forms.HiddenInput()
    
    return render(request, 'applications/program_form.html', {
        'form': form,
        'program': program
    })

# Application Views
@login_required
def application_list(request):
    # Regular users see only their applications
    if request.user.role == 'applicant':
        applications = Application.objects.filter(applicant=request.user)
    # University admins see applications for their university's programs
    elif request.user.role == 'university_admin':
        if not request.user.university:
            messages.error(request, 'You need to be assigned to a university to view applications.')
            return redirect('dashboard:dashboard')
        applications = Application.objects.filter(program__university=request.user.university)
    # System admins see all applications
    elif request.user.role == 'system_admin':
        applications = Application.objects.all()
    else:
        messages.error(request, 'You do not have permission to view applications.')
        return redirect('dashboard:dashboard')
    
    # Handle filtering
    status_filter = request.GET.get('status')
    if status_filter and status_filter != 'all':
        applications = applications.filter(status=status_filter)
    
    # Get application statistics
    stats = {
        'all': applications.count(),
        'draft': applications.filter(status='draft').count(),
        'submitted': applications.filter(status='submitted').count(),
        'approved': applications.filter(status='approved').count(),
        'rejected': applications.filter(status='rejected').count(),
        'pending': applications.filter(status='pending').count(),
    }
    
    # Order applications
    applications = applications.order_by('-submission_date', '-created_at')
    
    context = {
        'applications': applications,
        'stats': stats,
        'current_filter': status_filter or 'all',
    }
    
    return render(request, 'applications/application_list.html', context)

@login_required
def application_detail(request, pk):
    # Get the application without filtering by applicant
    application = get_object_or_404(Application, pk=pk)
    
    # Check permissions
    if not (request.user == application.applicant or 
            (request.user.role == 'university_admin' and request.user.university == application.program.university) or
            request.user.role == 'system_admin'):
        messages.error(request, 'You do not have permission to view this application.')
        return redirect('applications:application_list')
    
    # Get all required document types
    required_documents = ['transcript', 'diploma', 'passport', 'photo']
    submitted_documents = application.documents.values_list('document_type', flat=True)
    
    # Check which documents are missing
    missing_documents = [doc for doc in required_documents if doc not in submitted_documents]
    
    # Get document status counts
    document_status = {
        'verified': application.documents.filter(status='verified').count(),
        'pending': application.documents.filter(status='pending').count(),
        'rejected': application.documents.filter(status='rejected').count(),
    }
    
    context = {
        'application': application,
        'required_documents': required_documents,
        'submitted_documents': submitted_documents,
        'missing_documents': missing_documents,
        'document_status': document_status,
        'can_submit': not missing_documents and application.status == 'draft',
        'can_edit': application.status == 'draft' and request.user == application.applicant,
    }
    
    return render(request, 'applications/application_detail.html', context)

@login_required
def application_create(request, program_pk):
    program = get_object_or_404(Program, pk=program_pk)
    
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.applicant = request.user
            application.program = program
            application.status = 'draft'
            application.save()
            messages.success(request, 'Application created successfully.')
            return redirect('applications:application_detail', pk=application.pk)
        else:
            # Add form error messages
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'Error in {field}: {error}')
    else:
        form = ApplicationForm()
    
    return render(request, 'applications/application_form.html', {
        'form': form,
        'program': program
    })

@login_required
def application_update(request, pk):
    application = get_object_or_404(Application, pk=pk, applicant=request.user)
    
    if application.status != 'draft':
        messages.error(request, 'Only draft applications can be updated.')
        return redirect('applications:application_detail', pk=application.pk)
    
    if request.method == 'POST':
        form = ApplicationForm(request.POST, instance=application)
        if form.is_valid():
            form.save()
            messages.success(request, 'Application updated successfully.')
            return redirect('applications:application_detail', pk=application.pk)
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
        return redirect('applications:application_detail', pk=application.pk)
    
    required_documents = ['transcript', 'diploma', 'passport', 'photo']
    submitted_documents = application.documents.values_list('document_type', flat=True)
    
    missing_documents = [doc for doc in required_documents if doc not in submitted_documents]
    
    if missing_documents:
        messages.error(request, f'Please upload the following required documents: {", ".join(missing_documents)}')
        return redirect('applications:application_detail', pk=application.pk)
    
    application.status = 'submitted'
    application.submission_date = timezone.now()
    application.save()
    
    messages.success(request, 'Application submitted successfully.')
    return redirect('applications:application_detail', pk=application.pk)

# Document Views
@login_required
def document_upload(request, application_pk):
    application = get_object_or_404(Application, pk=application_pk, applicant=request.user)
    
    if application.status != 'draft':
        messages.error(request, 'Documents can only be uploaded for draft applications.')
        return redirect('applications:application_detail', pk=application.pk)
    
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.application = application
            document.save()
            messages.success(request, 'Document uploaded successfully.')
            return redirect('applications:application_detail', pk=application.pk)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'Error in {field}: {error}')
    else:
        form = DocumentForm()
    
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
            
            return redirect('applications:application_review', pk=document.application.pk)
    else:
        form = DocumentVerificationForm(instance=document)
    
    return render(request, 'applications/document_verify.html', {
        'form': form,
        'document': document
    })

# Review Views
@login_required
def application_review(request, pk):
    # Get the application
    application = get_object_or_404(Application, pk=pk)
    
    # Check if user has permission to review
    if not (request.user.role == 'university_admin' and request.user.university == application.program.university):
        messages.error(request, 'You do not have permission to review this application.')
        return redirect('applications:application_list')
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in ['approved', 'rejected', 'pending']:
            # Update application status
            application.status = new_status
            application.reviewed_by = request.user
            application.reviewed_at = timezone.now()
            application.save()
            
            # Send notification to the applicant
            messages.success(request, f'Application status updated to {application.get_status_display()}.')
        else:
            messages.error(request, 'Invalid status provided.')
    
    return redirect('applications:application_detail', pk=pk)

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

@login_required
def university_create(request):
    # Allow system admins or university admins without an assigned university
    if not (request.user.role == 'system_admin' or 
            (request.user.role == 'university_admin' and not request.user.university)):
        messages.error(request, 'You do not have permission to create universities.')
        return redirect('dashboard:dashboard')

    if request.method == 'POST':
        form = UniversityForm(request.POST, request.FILES)
        if form.is_valid():
            university = form.save()
            
            # If user is university admin, assign them to the created university
            if request.user.role == 'university_admin':
                request.user.university = university
                request.user.save()
            
            messages.success(request, 'University created successfully.')
            return redirect('applications:university_detail', pk=university.pk)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'Error in {field}: {error}')
    else:
        form = UniversityForm()

    return render(request, 'applications/university_form.html', {'form': form})

@login_required
def university_detail(request, pk):
    university = get_object_or_404(UniversitiesUniversity, pk=pk)
    return render(request, 'applications/university_detail.html', {
        'university': university
    })

@login_required
def university_list(request):
    universities = UniversitiesUniversity.objects.all()
    return render(request, 'applications/university_list.html', {
        'universities': universities
    })

@login_required
def university_update(request, pk):
    university = get_object_or_404(UniversitiesUniversity, pk=pk)
    
    # Check if user has permission to update this university
    if not (request.user.role == 'system_admin' or 
            (request.user.role == 'university_admin' and request.user.university == university)):
        messages.error(request, 'You do not have permission to update this university.')
        return redirect('dashboard:dashboard')
    
    if request.method == 'POST':
        form = UniversityForm(request.POST, request.FILES, instance=university)
        if form.is_valid():
            form.save()
            messages.success(request, 'University updated successfully.')
            return redirect('applications:university_detail', pk=university.pk)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'Error in {field}: {error}')
    else:
        form = UniversityForm(instance=university)
    
    return render(request, 'applications/university_form.html', {
        'form': form,
        'university': university
    })

@login_required
def contact_university(request, university_pk):
    university = get_object_or_404(University, pk=university_pk)
    
    if request.method == 'POST':
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        if not subject or not message:
            messages.error(request, 'Please fill in all required fields.')
            return redirect('applications:university_detail', pk=university.pk)
        
        # Create a message to the university
        Message.objects.create(
            sender=request.user,
            recipient=university.contact_email,
            subject=f"[University Contact] {subject}",
            content=message
        )
        
        messages.success(request, 'Your message has been sent to the university.')
        return redirect('applications:university_detail', pk=university.pk)
    
    return redirect('applications:university_detail', pk=university.pk)

@login_required
def request_info(request, university_pk):
    university = get_object_or_404(University, pk=university_pk)
    
    if request.method == 'POST':
        info_type = request.POST.get('info_type')
        notes = request.POST.get('notes', '')
        
        if not info_type:
            messages.error(request, 'Please select an information type.')
            return redirect('applications:university_detail', pk=university.pk)
        
        # Create a message to the university
        Message.objects.create(
            sender=request.user,
            recipient=university.contact_email,
            subject=f"[Information Request] {info_type}",
            content=f"Information Type: {info_type}\n\nAdditional Notes:\n{notes}"
        )
        
        messages.success(request, 'Your information request has been sent to the university.')
        return redirect('applications:university_detail', pk=university.pk)
    
    return redirect('applications:university_detail', pk=university.pk)

@login_required
def document_update(request, pk):
    document = get_object_or_404(Document, pk=pk)
    
    # Check if user owns this document's application
    if document.application.applicant != request.user:
        messages.error(request, 'You do not have permission to update this document.')
        return redirect('applications:application_detail', pk=document.application.pk)
    
    # Check if application is still in draft status
    if document.application.status != 'draft':
        messages.error(request, 'Documents can only be updated for draft applications.')
        return redirect('applications:application_detail', pk=document.application.pk)
    
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES, instance=document)
        if form.is_valid():
            form.save()
            messages.success(request, 'Document updated successfully.')
            return redirect('applications:application_detail', pk=document.application.pk)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'Error in {field}: {error}')
    else:
        form = DocumentForm(instance=document)
    
    return render(request, 'applications/document_form.html', {
        'form': form,
        'application': document.application,
        'document': document
    })
