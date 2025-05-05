from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from applications.models import Application, Program
from universities.models import University
from django.utils import timezone
from django.core.paginator import Paginator
from django.db.models import Q, Count, Prefetch

# Create your views here.

@login_required
def dashboard(request):
    context = {
        'user': request.user,
        'now': timezone.now(),
    }
    
    # Get applications based on user role
    if request.user.role == 'student':
        # Students see their own applications
        context['applications'] = Application.objects.filter(applicant=request.user).order_by('-created_at')
    elif request.user.role == 'university_admin' and request.user.university:
        # University admins see applications for their university's programs
        context['applications'] = Application.objects.filter(program__university=request.user.university).order_by('-created_at')
        context['programs'] = Program.objects.filter(university=request.user.university).select_related('university').prefetch_related('applications').order_by('-created_at')
        context['universities'] = University.objects.filter(id=request.user.university.id)
    elif request.user.role == 'system_admin':
        # System admins see all applications
        context['applications'] = Application.objects.all().order_by('-created_at')
        context['programs'] = Program.objects.all().select_related('university').prefetch_related('applications').order_by('-created_at')
        context['universities'] = University.objects.all().order_by('name')
    
    # Get application statistics
    if 'applications' in context:
        context['total_applications'] = context['applications'].count()
        context['pending_applications'] = context['applications'].filter(status='pending').count()
        context['approved_applications'] = context['applications'].filter(status='approved').count()
        context['rejected_applications'] = context['applications'].filter(status='rejected').count()
    
    return render(request, 'dashboard/dashboard.html', context)

@login_required
def university_management(request):
    # Get search query
    search_query = request.GET.get('search', '')
    
    # Get filter parameters
    selected_country = request.GET.get('country', '')
    selected_type = request.GET.get('type', '')
    
    # Get all universities with program counts
    universities = University.objects.annotate(
        program_count=Count('program', distinct=True),
        student_count=Count('program__application', distinct=True)
    ).all()
    
    # Apply search filter
    if search_query:
        universities = universities.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(city__icontains=search_query)
        )
    
    # Apply country filter
    if selected_country:
        universities = universities.filter(country=selected_country)
    
    # Apply type filter
    if selected_type:
        universities = universities.filter(type=selected_type)
    
    # Get unique countries for filter dropdown
    countries = University.objects.exclude(country__isnull=True).values_list('country', flat=True).distinct()
    countries = [{'code': country, 'name': country} for country in countries]
    
    # Get university types for filter dropdown
    university_types = University.TYPE_CHOICES
    
    # Pagination
    paginator = Paginator(universities, 10)  # Show 10 universities per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'countries': countries,
        'university_types': university_types,
        'selected_country': selected_country,
        'selected_type': selected_type,
    }
    
    return render(request, 'dashboard/university_management.html', context)
