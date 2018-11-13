from django.shortcuts import render
from rest_framework import viewsets, views
from .serializers import ResponseSerializer
from .models import Response, Question
from django.db.models import Count
from django.http import JsonResponse

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

class QCountView(views.APIView):
    """
    GET method handler
    """
    def get(self, request, format='json'):
        q_counts = Response.objects.values('q').annotate(total=Count('q')).order_by('q')
        return JsonResponse({'results': list(q_counts)})
    # queryset = Response.objects.all()
    # serializer_class = QCountSerializer
