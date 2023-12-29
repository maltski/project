from datetime import datetime
import logging
from django.db import connection
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from polls.forms import AddQuestionForm, LoginForm, RegistrationForm
from .models import Choice, Question
from django.contrib.auth import logout

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']

            if password == confirm_password:
                if not User.objects.filter(username=username).exists():
                    User.objects.create(username=username, password=password)

                    return redirect('login')
                else:
                    return render(request, 'polls/register.html', {'form': form, 'error_message': 'Username already taken'})
            else:
                return render(request, 'polls/register.html', {'form': form, 'error_message': 'Passwords do not match'})
    else:
        form = RegistrationForm()

    return render(request, 'polls/register.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = User.objects.filter(username=username, password=password).first()

            if user:
                #logging.debug(f'User {username} succeeded to log in')
                return redirect('index')
            else:
                #logging.debug(f'User {username} failed to log in')
                return render(request, 'polls/login.html', {'form': form, 'error_message': 'Invalid credentials'})
    else:
        form = LoginForm()

    return render(request, 'polls/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('polls:login')


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

def mystery(request):
    raise Exception("This is a deliberate error to test DEBUG setting")


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()

        return HttpResponseRedirect(reverse('results', args=(question.id,)))


def addquestion(request):
    question = request.GET.get("q") #POST
    choice1 = request.GET.get("c1") #POST
    choice2 = request.GET.get("c2") #POST
    q = Question(question_text=question, pub_date=datetime.now())
    q.save()
    q.choice_set.create(choice_text=choice1, votes=0)
    q.choice_set.create(choice_text=choice2, votes=0)
    q.save()
    form = AddQuestionForm(request.GET) #POST

    return render(request, 'polls/addquestion.html', {'form': form})
