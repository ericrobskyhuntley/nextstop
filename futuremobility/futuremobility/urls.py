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
router.register(r'random', views.RandomCardViewSet, basename='random-list')
router.register(r'qcount', views.QCountViewSet)
# router.register(r'random/(?P<q>)/$', views.RandomCardViewSet, basename='random-list')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/admin/')),
    url(r'^', include(router.urls)),
    # url('^random/(?P<q>.+)/$', views.RandomCardViewSet),
    #  namespace='rest_framework')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
