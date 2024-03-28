from django.urls import path, re_path
from core.views import LogInView,LogOutView, RegisterView
app_name = 'core'

urlpatterns = [
   path('auth/login/', LogInView, name='login'),
   path('auth/logout/', LogOutView, name='logout'),
   path('auth/register/', RegisterView, name='signup')
]