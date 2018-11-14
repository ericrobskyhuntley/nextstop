from rest_framework import serializers
from .models import Response, Question, Answer


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('answer',)

class ResponseSerializer(serializers.ModelSerializer):

    q_text = serializers.CharField(source='q.question')
    a = TagSerializer(read_only=True, many=True)
    s_text = serializers.CharField(source='survey.name')
    free_q_text = serializers.CharField(source='free_q.free_question')


    class Meta:
        model = Response
        fields = ('id', 'q_text', 'a', 'gender', 'aizersge', 'zip_code', 'home', 'free_q_text', 'free_resp', 's_text', 'timestamp', 'front', 'back', )

class QCountSerializer(serializers.Serializer):

    question = serializers.SerializerMethodField()
    total = serializers.IntegerField()

    def get_question(self, obj):
        return Question.objects.filter(id=obj['q']).values_list('question', flat=True)[0]
