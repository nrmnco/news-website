from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('news-today/', views.breaking_news, name='breaking_news'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('sign-in/', views.sign_in, name='sign_in'),
    path('verify_news/', views.verify_news_view, name='verify'),
    path('parse-articles/', views.parse_articles, name='parse_articles'),
]
