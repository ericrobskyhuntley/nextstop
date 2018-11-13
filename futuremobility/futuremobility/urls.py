"""futuremobility URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
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
router.register(r'randomcard', views.RandomCardViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('survey/', include('survey.urls')),
    path('', RedirectView.as_view(url='/admin/')),
    # re_path('api/(?P<version>(v1|v2))/', include('survey.urls')),
    url(r'^', include(router.urls)),
    url(r'^qcount/$', views.QCountView.as_view()),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
