from django.urls import path, include
from . import views

URL_NAME_PREFIX = ''

urlpatterns = [
    path('replicas/', include('replicas.api.urls')),
]