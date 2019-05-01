from django.contrib import admin

# Models
from replicas.models import Replica

class ReplicaAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', ]

admin.site.register(Replica, ReplicaAdmin)
