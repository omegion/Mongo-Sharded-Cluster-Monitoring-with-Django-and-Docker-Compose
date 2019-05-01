from django.urls import path, include

from replicas.api import views

URL_NAME_PREFIX = 'api.replicas'

urlpatterns = [
    path('', views.ListReplica.as_view(), name=URL_NAME_PREFIX + 'replicas.index'),
    path('<int:pk>/drop/', views.DropReplicaView.as_view(), name=URL_NAME_PREFIX + 'replicas.drop'),
    path('query/', views.QueryView.as_view(), name=URL_NAME_PREFIX + 'replicas.query'),
    path('checks/', views.ListCheck.as_view(), name=URL_NAME_PREFIX + 'checks.index'),
]