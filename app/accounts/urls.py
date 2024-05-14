from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('my-profile/', views.my_profile, name='my_profile')
]