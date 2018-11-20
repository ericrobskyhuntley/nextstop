import factory
import factory.django
import factory.fuzzy
import random
from survey.models import Question, Answer, Survey, Response, FreeQuestion

class QuestionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Question
        django_get_or_create = ['id',]

    id = 5

class SurveyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Survey
        django_get_or_create = ['id',]

    id = 2

class FreeQuestionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = FreeQuestion
        django_get_or_create = ['id',]

    id = 2


class ResponseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Response

    q = factory.SubFactory(QuestionFactory)
    @factory.post_generation
    def a(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return
        if extracted:
            # A list of groups were passed in, use them
            for answer in extracted:
                self.a.add(answer)
    gender = factory.fuzzy.FuzzyChoice(['nonbinary', 'female', 'male'])
    age = factory.fuzzy.FuzzyChoice(['under-18', '18-24', '25-34', '35-44', '45-54', '55-64', '65-plus'])
    zip_code = factory.Faker('zipcode')
    free_q = factory.SubFactory(FreeQuestionFactory)
    free_resp = ''
    survey = factory.SubFactory(SurveyFactory)
    front = 'static/templates/q04-front.png'
    back = 'static/templates/q04-back.png'
