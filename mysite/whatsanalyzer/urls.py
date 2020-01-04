from django.urls import path

from . import views

# Creates a custom namespace to allow Django to know which app's view to execute
app_name = 'whatsanalyzer'

urlpatterns = [
    path('', views.index, name='index'),
    path('charts/', views.charts, name='charts'),
    path('metrics/', views.metrics, name='metrics'),
    path('stash/', views.stash, name='stash'),
]
