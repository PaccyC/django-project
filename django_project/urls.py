
from django.contrib import admin
from django.urls import path,include
from django.http import HttpResponse

  
urlpatterns = [
    path('admin/', admin.site.urls),
    path("",include('base.urls')),
    path("api/", include('base.api.urls'))
]
