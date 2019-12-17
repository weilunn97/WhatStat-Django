from django.urls import path

from . import views

# Creates a custom namespace to allow Django to know which app's view to execute
app_name = 'polls'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:question_id>/', views.details, name='details'),
    path('<int:question_id>/results/', views.results, name='results'),
    path('<int:question_id>/votes/', views.votes, name='votes'),
]
