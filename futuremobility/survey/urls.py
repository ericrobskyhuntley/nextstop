from django.urls import path
from .views import ListResponseView

urlpatterns = [
    path('responses/', ListResponseView.as_view(), name='responses-all')
]
