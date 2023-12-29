from django.urls import path
from django.contrib.auth.views import LoginView

from . import views

#app_name = 'polls'
urlpatterns = [
    path('polls/', views.index, name='index'),
    path('polls/<int:question_id>/', views.detail, name='detail'),
    path('polls/<int:question_id>/results/', views.results, name='results'),
    path('polls/<int:question_id>/vote/', views.vote, name='vote'),
    #path('', views.login, name='login'),
    path('', LoginView.as_view(), name='login_fixed'),
    path('polls/addquestion/', views.addquestion, name="addquestion"),
    #path('', views.user_logout, name="logout"),
    path('', views.user_logout_fixed, name="logout_fixed"),
    path('mystery', views.mystery, name="mystery"),
    #path('register', views.register, name='register')
]
