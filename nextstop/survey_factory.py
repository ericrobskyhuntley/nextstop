import factory
import factory.django
import factory.fuzzy
from survey.models import Question, Answer, Survey, Response

class QuestionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Question
        django_get_or_create = ['question', 'type']

    question = 'Right now, I’m feeling _______ about widespread autonomous vehicle use.'
    type = 'multiple-choice'

class AnswerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Answer
        django_get_or_create = ['q', 'answer']

    q = factory.SubFactory(QuestionFactory)
    answer = factory.fuzzy.FuzzyChoice(['Eager', 'Optimistic', 'Neutral', 'Anxious', 'Afraid'])

class SurveyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Survey
        django_get_or_create = ['name', 'desc']

    name = 'Pre-populate'
    desc = 'Pre-populating database for visualization test purposes.'

class ResponseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Response

    q = factory.SubFactory(QuestionFactory)
    a = factory.SubFactory(AnswerFactory)
    survey = factory.SubFactory(SurveyFactory)
    scan = '~/test/test-001.png'
