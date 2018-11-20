from django.shortcuts import render
from rest_framework import  viewsets
from django.db.models import Count
from .models import Response
from .serializers import ResponseSerializer, QCountSerializer, QACountSerializer

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

class QACountViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only API endpoint returning a list of questions and a total number of responses to each question.
    """
    serializer_class = QACountSerializer
    def get_queryset(self):
        q_query = self.request.query_params.get('q', None)
        if q_query is not None:
            queryset = Response.objects.raw( 'SELECT survey_response.q_id, survey_response_a.answer_id AS id, COUNT(*) AS total FROM survey_response, survey_response_a WHERE (survey_response.id = survey_response_a.response_id) AND (survey_response.q_id=' + q_query + ') GROUP BY survey_response.q_id, survey_response_a.answer_id ORDER BY survey_response.q_id, id;')
        else:
            queryset = Response.objects.raw( 'SELECT survey_response.q_id, survey_response_a.answer_id AS id, min(survey_answer.answer) AS a_text, COUNT(*) AS total FROM survey_response, survey_response_a, survey_answer WHERE (survey_response.id = survey_response_a.response_id) AND (survey_response_a.answer_id = survey_answer.id) GROUP BY survey_response.q_id, survey_response_a.answer_id ORDER BY survey_response.q_id, id;')
        return queryset

class QCountViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only API endpoint returning a list of questions and a total number of responses to each question.
    """
    queryset = Response.objects.values('q').annotate(total=Count('q')).order_by('q')
    serializer_class = QCountSerializer
