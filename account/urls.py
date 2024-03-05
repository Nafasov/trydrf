from django.urls import path
from rest_framework.authtoken import views as token_auth_view


app_name = 'account'

urlpatterns = [
    path('login/', token_auth_view.obtain_auth_token, name='login'),
]

