from django.views.generic import TemplateView, ListView, DetailView 
from django.shortcuts import render
from django.conf import settings

from replicas.models import Replica

class IndexView(TemplateView):
    template_name = "replicas/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'MongoDB'
        context['description'] = 'Knowledgebase of Crawly'
        return context