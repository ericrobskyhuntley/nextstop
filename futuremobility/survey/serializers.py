from rest_framework import serializers
from .models import Response, Question

class ResponseSerializer(serializers.ModelSerializer):

    q_text = serializers.CharField(source='q.question')
    a_text = serializers.CharField(source='a.answer')
    s_text = serializers.CharField(source='survey.name')


    class Meta:
        model = Response
        fields = ('id', 'q_text', 'a_text', 'timestamp', 'scan', 's_text')
