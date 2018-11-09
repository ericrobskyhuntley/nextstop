from django.contrib import admin

from survey.models import Survey, Response, Question, Answer

class SurveyAdmin(admin.ModelAdmin):
    list_display = ('name', 'desc')
admin.site.register(Survey, SurveyAdmin)

class ResponseAdmin(admin.ModelAdmin):
    list_display = ('id', 'timestamp', 'q', 'a', 'front', 'back')
admin.site.register(Response, ResponseAdmin)

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'type')
admin.site.register(Question, QuestionAdmin)

class AnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'answer', 'q')
admin.site.register(Answer, AnswerAdmin)
