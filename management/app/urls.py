from django.urls import path
from .views import Register, LogIn, Home, UpdateProfile, logout, delete, login_api
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', Register.as_view(), name='register'),
    path('login', LogIn.as_view(), name='login'),
    path('login_api', login_api, name='login_api'),
    path('homepage', Home.as_view(), name='homepage'),
    path('update', UpdateProfile.as_view(), name='update'),
    path('logout', logout, name='logout'),
    path('delete', delete, name='delete'),
]
