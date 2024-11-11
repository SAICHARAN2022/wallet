from django.urls import path
from . import views 
from django.shortcuts import redirect
from django.urls import path

from django.urls import path
from django.contrib.auth.views import LoginView
from . import views
from . import views





urlpatterns = [
    path('login/', views.login_view.as_view(), name='login'), 
    path('signup/', views.RegisterView.as_view(), name='signup'),
    path('home/', views.WalletView.as_view(), name='wallet'),
    path('deposit/',views.AddFundsView.as_view(), name='deposit'),
    path('withdraw/', views.SubtractFundsView.as_view(), name='withdraw'),
    path('enable_status/', views.enable_status.as_view(), name='withdraw'),
    
]
