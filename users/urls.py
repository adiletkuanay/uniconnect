from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('profile/upload-document/', views.upload_document, name='upload_document'),
    path('settings/', views.settings, name='settings'),
    path('delete-account/', views.delete_account, name='delete_account'),
] 