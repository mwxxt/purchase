from django.urls import path
from account import views

urlpatterns = [
    path('users/', views.UserAPIView.as_view()),
    path('user/<int:id>/', views.UserDetailAPIView.as_view()),
    path('profiles/', views.ProfileAPIView.as_view()),
    path('profile/<int:id>/', views.ProfileDetailAPIView.as_view())
    
]