from django.urls import path
from .views import PasswordCreateRetrieveGetView, PasswordSearchView
urlpatterns = [
    path('password/<str:service_name>', PasswordCreateRetrieveGetView.as_view(), name='password-get-post'),
    path('password/', PasswordSearchView.as_view(), name='pass-search'),
]