from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login_view, name="login"),  # Add login URL
    path("logout/", views.logout_view, name="logout"),  # Add logout URL
    path("about-us/", views.about_us, name="about_us"),
    path('register/', views.register_view, name='register'),
    path('quiz/', views.quiz, name='quiz'),
    path('review-us/', views.review_us, name='review_us'),
    
]
