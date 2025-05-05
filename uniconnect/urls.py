"""
URL configuration for uniconnect project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin URLs
    path('admin/', admin.site.urls),
    
    # Authentication URLs
    path('accounts/', include('allauth.urls')),  # django-allauth URLs
    
    # Core URLs (including home page)
    path('', include('core.urls')),
    
    # Application URLs
    path('applications/', include('applications.urls')),
    
    # Users URLs
    path('users/', include('users.urls')),
    
    # Dashboard URLs
    path('dashboard/', include('dashboard.urls')),
    
    # Universities URLs
    path('universities/', include('universities.urls')),
    
    # API URLs (if needed in the future)
    # path('api/', include('applications.api.urls')),
]

# Serve static and media files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
