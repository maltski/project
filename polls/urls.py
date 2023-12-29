from django.urls import path
from django.contrib.auth.views import LoginView

from . import views


urlpatterns = [
    path('polls/', views.index, name='index'),
    path('polls/<int:question_id>/', views.detail, name='detail'),
    path('polls/<int:question_id>/results/', views.results, name='results'),
    path('polls/<int:question_id>/vote/', views.vote, name='vote'),
    path('', views.login, name='login'),
    path('polls/addquestion/', views.addquestion, name="addquestion"),
    path('', views.user_logout, name="logout"),
    path('mystery', views.mystery, name="mystery"),
    path('register', views.register, name='register')
]
