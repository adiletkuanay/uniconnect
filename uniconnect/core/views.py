from django.shortcuts import render
from django.db.models import Count
from universities.models import University, Program
from applications.models import Application

def home(request):
    # Get statistics for the homepage
    stats = {
        'universities_count': University.objects.count(),
        'programs_count': Program.objects.count(),
        'applications_count': Application.objects.count(),
    }
    
    # Get featured universities (top 5 by ranking)
    featured_universities = University.objects.filter(
        ranking__isnull=False
    ).order_by('ranking')[:5]
    
    # Get popular programs (top 5 by application count)
    popular_programs = Program.objects.annotate(
        application_count=Count('applications')
    ).order_by('-application_count')[:5]
    
    context = {
        'stats': stats,
        'featured_universities': featured_universities,
        'popular_programs': popular_programs,
    }
    return render(request, 'core/home.html', context)

def about(request):
    return render(request, 'core/about.html')

def contact(request):
    return render(request, 'core/contact.html')

def privacy(request):
    return render(request, 'core/privacy.html')
