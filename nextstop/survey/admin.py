from django.contrib import admin

from survey.models import Survey, Response, Question, FreeQuestion, Answer

class SurveyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'desc')
admin.site.register(Survey, SurveyAdmin)

class ResponseAdmin(admin.ModelAdmin):
    list_display = ('id', 'timestamp', 'q', 'get_answers', 'front', 'back')
    def get_answers(self, obj):
        return "\n".join([a.answer for a in obj.a.all()])
admin.site.register(Response, ResponseAdmin)

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'question_type')
admin.site.register(Question, QuestionAdmin)

class FreeQuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'free_question')
admin.site.register(FreeQuestion, FreeQuestionAdmin)

class AnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'answer', 'get_questions')
    def get_questions(self, obj):
        return "\n".join([q.question for q in obj.q.all()])
admin.site.register(Answer, AnswerAdmin)
