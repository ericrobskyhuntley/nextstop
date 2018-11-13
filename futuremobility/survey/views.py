from django.shortcuts import render
from rest_framework import viewsets
from .serializers import ResponseSerializer
from .models import Response, Question

class ResponseViewSet(viewsets.ModelViewSet):
    """
    GET method handler
    """
    queryset = Response.objects.all()
    serializer_class = ResponseSerializer

class RandomCardViewSet(viewsets.ModelViewSet):
    """
    GET method handler
    """
    queryset = Response.objects.order_by('?')[:1]
    serializer_class = ResponseSerializer
