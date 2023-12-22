from datetime import datetime
from django import forms
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Choice, Question
from django.contrib.auth import logout
from django.utils.html import escape


def user_logout(request):
    logout(request)
    return redirect('polls:login')

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput())

def user_login(request):
    return render(request, 'polls/login.html')


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


class AddQuestionForm(forms.Form):
    question = forms.CharField(max_length=200)
    choice1 = forms.CharField(max_length=200)
    choice2 = forms.CharField(max_length=200)
    password = forms.CharField(max_length=200, widget=forms.PasswordInput())

def addquestion(request):
    question = request.GET.get("q")
    choice1 = request.GET.get("c1")
    choice2 = request.GET.get("c2")

    q = Question(question_text=question, pub_date=datetime.now())
    q.save()
    q.choice_set.create(choice_text=choice1, votes=0)
    q.choice_set.create(choice_text=choice2, votes=0)
    q.save()
    form = AddQuestionForm()
    return render(request, 'polls/index.html', {'form': form})


# Fix for addquestion:

#def addquestion(request):
#    if request.method == 'POST':
#        form = AddQuestionForm(request.POST)
#        if form.is_valid():
#            question_text = escape(form.cleaned_data['question'])
#            choice1_text = escape(form.cleaned_data['choice1'])
#            choice2_text = escape(form.cleaned_data['choice2'])

#            q = Question(question_text=question_text, pub_date=datetime.now())
#            q.save()
#            q.choice_set.create(choice_text=choice1_text, votes=0)
#            q.choice_set.create(choice_text=choice2_text, votes=0)
#            q.save()

#            return redirect("polls/")
#    else:
#        form = AddQuestionForm()

#    return render(request, 'polls/index.html', {'form': form})
