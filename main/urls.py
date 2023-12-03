from django.urls import path
from .views import PasswordCreateRetrieveGetView, PasswordSearchView
urlpatterns = [
    path('password/<str:service_name>', PasswordCreateRetrieveGetView.as_view()),
    path('password/', PasswordSearchView.as_view()),
]