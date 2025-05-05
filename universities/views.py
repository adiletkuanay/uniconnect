from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import University
from applications.models import Program, Document
from .forms import UniversityForm
from django.http import JsonResponse
import os

# Create your views here.

@login_required
def university_create(request):
    # if not request.user.is_staff:
    #     messages.error(request, 'You do not have permission to create universities.')
    #     return redirect('universities:university_list')
    
    if request.method == 'POST':
        form = UniversityForm(request.POST, request.FILES)
        if form.is_valid():
            university = form.save()
            messages.success(request, 'University created successfully.')
            return redirect('universities:university_detail', pk=university.pk)
    else:
        form = UniversityForm()
    
    return render(request, 'universities/university_form.html', {'form': form})

@login_required
def university_list(request):
    universities = University.objects.all()
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        universities = universities.filter(
            Q(name__icontains=search_query) |
            Q(city__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Filter by country
    selected_country = request.GET.get('country', '')
    if selected_country:
        universities = universities.filter(country=selected_country)
    
    # Filter by type
    selected_type = request.GET.get('type', '')
    if selected_type:
        universities = universities.filter(type=selected_type)
    
    # Get unique countries from universities
    countries = University.objects.exclude(
        country__isnull=True
    ).values_list('country', flat=True).distinct().order_by('country')
    
    # Get university types from model choices
    university_types = University.TYPE_CHOICES
    
    # Pagination
    paginator = Paginator(universities, 9)  # Show 9 universities per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'countries': [{'code': country, 'name': country} for country in countries],
        'university_types': university_types,
        'selected_country': selected_country,
        'selected_type': selected_type,
    }
    return render(request, 'universities/university_list.html', context)

@login_required
def university_detail(request, pk):
    university = get_object_or_404(University, pk=pk)
    programs = Program.objects.filter(university=university)
    context = {
        'university': university,
        'programs': programs,
    }
    return render(request, 'universities/university_detail.html', context)

@login_required
def program_list(request, pk):
    university = get_object_or_404(University, pk=pk)
    programs = Program.objects.filter(university=university)
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        programs = programs.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(field_of_study__icontains=search_query)
        )
    
    # Filter by degree level
    degree_level = request.GET.get('degree_level')
    if degree_level:
        programs = programs.filter(degree_level=degree_level)
    
    # Filter by language
    language = request.GET.get('language')
    if language:
        programs = programs.filter(language=language)
    
    # Pagination
    paginator = Paginator(programs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'university': university,
        'page_obj': page_obj,
        'search_query': search_query,
        'degree_level': degree_level,
        'language': language,
    }
    return render(request, 'universities/program_list.html', context)

@login_required
def university_update(request, pk):
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to update universities.')
        return redirect('universities:university_list')
    
    university = get_object_or_404(University, pk=pk)
    
    if request.method == 'POST':
        form = UniversityForm(request.POST, request.FILES, instance=university)
        if form.is_valid():
            form.save()
            messages.success(request, 'University updated successfully.')
            return redirect('universities:university_detail', pk=university.pk)
    else:
        form = UniversityForm(instance=university)
    
    return render(request, 'universities/university_form.html', {'form': form})

@login_required
def university_delete(request, pk):
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to delete universities.')
        return redirect('universities:university_list')
    
    university = get_object_or_404(University, pk=pk)
    
    if request.method == 'POST':
        university.delete()
        messages.success(request, 'University deleted successfully.')
        return redirect('universities:university_list')
    
    return render(request, 'universities/university_confirm_delete.html', {'university': university})

@login_required
def upload_document(request, pk):
    university = get_object_or_404(University, pk=pk)
    
    if request.method == 'POST':
        if 'document' in request.FILES:
            document = request.FILES['document']
            # Check file type
            allowed_types = ['application/pdf', 'application/msword', 
                           'application/vnd.openxmlformats-officedocument.wordprocessingml.document']
            
            if document.content_type in allowed_types:
                # Create document object
                Document.objects.create(
                    university=university,
                    file=document,
                    uploaded_by=request.user
                )
                messages.success(request, 'Document uploaded successfully.')
                return redirect('universities:university_detail', pk=pk)
            else:
                messages.error(request, 'Invalid file type. Please upload PDF, DOC, or DOCX files only.')
        else:
            messages.error(request, 'Please select a document to upload.')
    
    return render(request, 'universities/document_form.html', {
        'university': university
    })
