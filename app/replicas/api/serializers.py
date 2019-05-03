from django.core.management import call_command
from django.conf import settings
from django.db.models import F
from rest_framework import serializers
from datetime import datetime, timedelta

# Models
from replicas.models import Replica, Check

class ReplicaSerializer(serializers.ModelSerializer):
    # user = serializers.SerializerMethodField()

    # def get_user(self, instance):
    #     return {
    #         'name': instance.user.name,
    #         'photo': self.context['request'].build_absolute_uri(instance.user.photo.url),
    #     }

    class Meta:
        model = Replica
        read_only_fields = ('id', 'name', 'shard', 'port', 'state', 'status', )
        fields = '__all__'

class CheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Check
        fields = '__all__'


class QuerySerializer(serializers.Serializer):
    query = serializers.CharField(required=True)

class QueryInsertSerializer(serializers.Serializer):
    number = serializers.IntegerField(required=True)
