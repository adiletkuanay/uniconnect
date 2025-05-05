from django.db.models import Q
from django.shortcuts import render
from universities.models import Program, University
from django.core.paginator import Paginator
from django.http import JsonResponse

def search_programs(request):
    query = request.GET.get('q', '')
    degree_level = request.GET.get('degree_level', '')
    field_of_study = request.GET.get('field_of_study', '')
    country = request.GET.get('country', '')
    language = request.GET.get('language', '')
    min_gpa = request.GET.get('min_gpa', '')
    scholarship = request.GET.get('scholarship', '')
    
    programs = Program.objects.all()
    
    if query:
        programs = programs.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(field_of_study__icontains=query) |
            Q(university__name__icontains=query)
        )
    
    if degree_level:
        programs = programs.filter(degree_level=degree_level)
    
    if field_of_study:
        programs = programs.filter(field_of_study__icontains=field_of_study)
    
    if country:
        programs = programs.filter(university__country=country)
    
    if language:
        programs = programs.filter(language=language)
    
    if min_gpa:
        programs = programs.filter(min_gpa__lte=float(min_gpa))
    
    if scholarship == 'true':
        programs = programs.filter(scholarship_available=True)
    
    # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(programs, 10)
    programs = paginator.get_page(page)
    
    context = {
        'programs': programs,
        'query': query,
        'degree_level': degree_level,
        'field_of_study': field_of_study,
        'country': country,
        'language': language,
        'min_gpa': min_gpa,
        'scholarship': scholarship,
    }
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'programs': [{
                'id': program.id,
                'title': program.title,
                'university': program.university.name,
                'degree_level': program.degree_level,
                'field_of_study': program.field_of_study,
                'duration': program.duration,
                'language': program.language,
                'min_gpa': program.min_gpa,
                'scholarship_available': program.scholarship_available,
                'url': program.get_absolute_url()
            } for program in programs],
            'has_next': programs.has_next(),
            'has_previous': programs.has_previous(),
            'page_number': programs.number,
            'total_pages': paginator.num_pages
        })
    
    return render(request, 'search/program_results.html', context)

def search_universities(request):
    query = request.GET.get('q', '')
    country = request.GET.get('country', '')
    university_type = request.GET.get('type', '')
    min_rank = request.GET.get('min_rank', '')
    max_rank = request.GET.get('max_rank', '')
    min_acceptance_rate = request.GET.get('min_acceptance_rate', '')
    max_acceptance_rate = request.GET.get('max_acceptance_rate', '')
    
    universities = University.objects.all()
    
    if query:
        universities = universities.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(city__icontains=query)
        )
    
    if country:
        universities = universities.filter(country=country)
    
    if university_type:
        universities = universities.filter(type=university_type)
    
    if min_rank:
        universities = universities.filter(rank__gte=int(min_rank))
    
    if max_rank:
        universities = universities.filter(rank__lte=int(max_rank))
    
    if min_acceptance_rate:
        universities = universities.filter(acceptance_rate__gte=float(min_acceptance_rate))
    
    if max_acceptance_rate:
        universities = universities.filter(acceptance_rate__lte=float(max_acceptance_rate))
    
    # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(universities, 10)
    universities = paginator.get_page(page)
    
    context = {
        'universities': universities,
        'query': query,
        'country': country,
        'university_type': university_type,
        'min_rank': min_rank,
        'max_rank': max_rank,
        'min_acceptance_rate': min_acceptance_rate,
        'max_acceptance_rate': max_acceptance_rate,
    }
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'universities': [{
                'id': university.id,
                'name': university.name,
                'country': university.country.name,
                'city': university.city,
                'type': university.type,
                'rank': university.rank,
                'acceptance_rate': university.acceptance_rate,
                'url': university.get_absolute_url()
            } for university in universities],
            'has_next': universities.has_next(),
            'has_previous': universities.has_previous(),
            'page_number': universities.number,
            'total_pages': paginator.num_pages
        })
    
    return render(request, 'search/university_results.html', context)

def autocomplete_programs(request):
    query = request.GET.get('q', '')
    if query:
        programs = Program.objects.filter(
            Q(title__icontains=query) |
            Q(field_of_study__icontains=query) |
            Q(university__name__icontains=query)
        )[:10]
        results = [{
            'id': program.id,
            'title': program.title,
            'university': program.university.name,
            'field_of_study': program.field_of_study
        } for program in programs]
    else:
        results = []
    
    return JsonResponse({'results': results})

def autocomplete_universities(request):
    query = request.GET.get('q', '')
    if query:
        universities = University.objects.filter(
            Q(name__icontains=query) |
            Q(city__icontains=query)
        )[:10]
        results = [{
            'id': university.id,
            'name': university.name,
            'city': university.city,
            'country': university.country.name
        } for university in universities]
    else:
        results = []
    
    return JsonResponse({'results': results}) 