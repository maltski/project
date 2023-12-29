from datetime import datetime
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from polls.forms import AddQuestionForm, LoginForm
from .models import Choice, Question
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = User.objects.filter(username=username, password=password).first()

            if user:
                return redirect('index')
            else:
                return render(request, 'polls/login.html', {'form': form, 'error_message': 'Invalid credentials'})
    else:
        form = LoginForm()

    return render(request, 'polls/login.html', {'form': form})


def user_logout_fixed(request):
    logout(request)
    return redirect('registration:login')

@login_required
def index(request):
    #latest_question_list = Question.objects.order_by('-pub_date')[:5]
    latest_question_list = Question.objects.filter(user=request.user).order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)


@login_required
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})


@login_required
def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

def mystery(request):
    raise Exception("This is a deliberate error to test DEBUG setting")


@login_required
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


@login_required
def addquestion(request):
    question = request.POST.get("q")
    choice1 = request.POST.get("c1")
    choice2 = request.POST.get("c2")
    user = request.user
    q = Question(question_text=question, pub_date=datetime.now(), user=user) # add  ', user=user' at the end inside outer parenthesis
    q.save()
    q.choice_set.create(choice_text=choice1, votes=0)
    q.choice_set.create(choice_text=choice2, votes=0)
    q.save()
    form = AddQuestionForm(request.POST)

    return render(request, 'polls/addquestion.html', {'form': form})
