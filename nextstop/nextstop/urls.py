from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls import url, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from survey import views

router = routers.DefaultRouter()
router.register(r'responses', views.ResponseViewSet)
# manually specifying basename is necessary because of the RandomCardViewSet class' custom get_queryset
router.register(r'random', views.RandomCardViewSet, basename='random-list')
router.register(r'qcount', views.QuestionCountViewSet)
router.register(r'qacount', views.AnswerCountViewSet, basename='qa-list')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/admin/')),
    url(r'^', include(router.urls)),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
