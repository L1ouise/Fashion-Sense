from django.urls import path
from .views import FashionRequestList

urlpatterns = [
    path('requests/', FashionRequestList.as_view(), name='fashion-request-list'),
]
