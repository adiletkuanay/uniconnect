from django.shortcuts import render
from django.db.models import Count
from applications.models import Application, Program
from users.models import CustomUser
from django.db.models import Avg
from django.contrib import messages
from django.urls import reverse
from django.shortcuts import redirect

def home(request):
    # Get statistics
    total_programs = Program.objects.count()
    total_universities = Program.objects.values('university').distinct().count()
    total_students = CustomUser.objects.filter(role='student').count()
    
    # Calculate success rate (approved applications)
    total_applications = Application.objects.count()
    approved_applications = Application.objects.filter(status='approved').count()
    success_rate = int((approved_applications / total_applications * 100) if total_applications > 0 else 0)
    
    # Get featured programs
    featured_programs = Program.objects.all()[:6]  # Get first 6 programs
    
    # Get testimonials (if you have them)
    testimonials = []  # Add your testimonial logic here if you have a testimonials model
    
    context = {
        'total_programs': total_programs,
        'total_universities': total_universities,
        'total_students': total_students,
        'success_rate': success_rate,
        'featured_programs': featured_programs,
        'testimonials': testimonials,
    }
    return render(request, 'home.html', context)

def about(request):
    return render(request, 'core/about.html')

def contact(request):
    return render(request, 'core/contact.html')

def privacy(request):
    return render(request, 'core/privacy.html')

def terms(request):
    return render(request, 'core/terms.html')

def support(request):
    if request.method == 'POST':
        # Handle contact form submission
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        # Here you would typically send an email or save to database
        messages.success(request, 'Your message has been sent. We will contact you soon!')
        return redirect('core:support')
        
    return render(request, 'core/support.html')
