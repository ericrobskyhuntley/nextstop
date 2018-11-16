from django.shortcuts import render
from rest_framework import  viewsets
from .serializers import ResponseSerializer, QCountSerializer
from .models import Response, Question
# from rest_framework.decorators import list_route
from rest_framework.decorators import action
from django.db.models import Count

class ResponseViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only API endpoint returning a list of all responses currently stored in database.
    """
    queryset = Response.objects.all()
    serializer_class = ResponseSerializer

class RandomCardViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only API endpoint returning a random card. An optional `q` query string parameter will filter possible responses to the question to which they respond.
    """
    # q = self.request.query_params.get('username', None)
    # queryset = Response.objects.order_by('?')[:1]
    serializer_class = ResponseSerializer
    def get_queryset(self):
        q_id = self.request.query_params.get('q', None)
        if q_id is not None:
            queryset = Response.objects.filter(q=q_id).order_by('?')[:1]
        else:
            queryset = Response.objects.all().order_by('?')[:1]
        return queryset

class QCountViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only API endpoint returning a list of questions and a total number of responses to each question.
    """
    queryset = Response.objects.values('q').annotate(total=Count('q')).order_by('q')
    serializer_class = QCountSerializer
