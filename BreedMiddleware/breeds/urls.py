from django.urls import path, re_path
from rest_framework.urlpatterns import format_suffix_patterns
from breeds import views

app_name = 'breads_api'

urlpatterns = [
    path('longest-lifespan-breed/', views.LongestBreeds.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)