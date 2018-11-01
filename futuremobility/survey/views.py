from django.shortcuts import render
from rest_framework import generics
from .serializers import ResponseSerializer
from .models import Response

class ListResponseView(generics.ListAPIView):
    """
    GET method handler
    """
    queryset = Response.objects.all()
    serializer_class = ResponseSerializer
