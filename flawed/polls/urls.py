from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('polls/', views.index, name='index'),
    path('<int:question_id>/', views.detail, name='detail'),
    path('<int:question_id>/results/', views.results, name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('', views.login, name='login'),
    path('polls/win/', views.win, name='win'),
]
