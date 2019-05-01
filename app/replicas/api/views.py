from uuid import uuid4
from urllib.parse import urlparse
from datetime import date

from django.shortcuts import render
from django.db.models import Q
from django.utils.text import slugify
from django.conf import settings
from rest_framework import generics, status, pagination, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly

# Models
from replicas.models import Replica, Check

# Serializers
from replicas.api import serializers

# Tasks
from replicas.tasks import replica_down, start_reading_from_replica

class ListReplica(generics.ListAPIView):
    serializer_class = serializers.ReplicaSerializer
    # filter_fields = ('is_active', 'category_id', )
    ordering = ('id')

    def get_queryset(self):
        page_size = self.request.GET.get('page_size', None)

        # set dynamic page size
        if page_size != None:
            pagination.PageNumberPagination.page_size = page_size
        
        return Replica.objects

class ListCheck(generics.ListAPIView):
    serializer_class = serializers.CheckSerializer
    filter_fields = ('replica_id', )
    ordering = ('id')

    def get_queryset(self):
        page_size = self.request.GET.get('page_size', None)

        # set dynamic page size
        if page_size != None:
            pagination.PageNumberPagination.page_size = page_size
        
        return Check.objects

class DropReplicaView(generics.CreateAPIView):
    serializer_class = serializers.ReplicaSerializer
    
    def get_queryset(self):
        site = Replica.objects
        return site

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        replica_down(instance.name)
        return Response({'replica' : ['Crawl request is received.', ]}, 
            status = status.HTTP_202_ACCEPTED)

class QueryView(APIView):
    serializer_class = serializers.QuerySerializer
    
    def get_queryset(self):
        site = Replica.objects
        return site

    def post(self, request, format=None):
        import ast
        query = request.data['query']

        my_dict = ast.literal_eval(query)

        result = start_reading_from_replica(query=my_dict)
        # replica_down(instance.name)
        return Response({'result' : result }, 
            status = status.HTTP_202_ACCEPTED)