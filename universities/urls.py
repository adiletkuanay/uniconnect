from django.urls import path
from . import views

app_name = 'universities'

urlpatterns = [
    path('create/', views.university_create, name='university_create'),
    path('list/', views.university_list, name='university_list'),
    path('<int:pk>/', views.university_detail, name='university_detail'),
    path('<int:pk>/update/', views.university_update, name='university_update'),
    path('<int:pk>/programs/', views.program_list, name='program_list'),
    path('<int:pk>/upload-document/', views.upload_document, name='upload_document'),
] 