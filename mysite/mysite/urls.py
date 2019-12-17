"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import include, path

'''
1. mysite/urls.py acts as a CONTROLLER to MAP URLs to views in your app(s)
2. Views DO NOT EXIST in your main site, only your created apps
3. To map URLs to individual apps, we perform an INCLUDE (~ import) of the urls.py 
file of the corresponding app that we wish to serve the user
'''
urlpatterns = [
    path('admin/', admin.site.urls),       # Default
    path('polls/', include('polls.urls'))  # "Importing" the polls app's url.py file
]
