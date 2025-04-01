from django.urls import path
from . import views

urlpatterns = [
    path('user-details', views.UserDetails.as_view(), name='user_details'),
    path('register', views.UserRegister.as_view(), name='user_register'),
    path('token/', views.TokenObtainView.as_view(), name='token_obtain'),
    path('token/refresh/', views.TokenRefreshView.as_view(), name='token_refresh'),
]