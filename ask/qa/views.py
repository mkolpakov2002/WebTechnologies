from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage
from django.contrib.auth import authenticate, login

from .models import Question, Answer
from .forms import *

def test(request, *args, **kwargs):
    return HttpResponse('OK')

def new(request):
    try:
        page = int(request.GET.get('page', 1))
    except:
        page = 1
    limit = 10

    questions = Question.objects.new()
    paginator = Paginator(questions, limit)

    try:
        page = paginator.page(page)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        page = paginator.page(paginator.num_pages)

    return render(request, "posts/index.html", {
        'page': page
    })

def popular(request):
    try:
        page = int(request.GET.get('page', 1))
    except:
        page = 1
    limit = 10

    questions = Question.objects.popular()
    paginator = Paginator(questions, limit)

    try:
        page = paginator.page(page)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        page = paginator.page(paginator.num_pages)

    return render(request, "posts/index.html", {
        'page': page
    })

def question(request, id):
    try:
        questionId = int(id)
    except:
        raise Http404

    try:
        question = Question.objects.get(pk=questionId)
    except:
        raise Http404

    if request.method == "POST":
        form = AnswerForm(request.POST)
        form._user = request.user
        if form.is_valid():
            answer = form.save()
            url = question.get_url()
            return HttpResponseRedirect(url)
    else:
        form = AnswerForm()

    answers = Answer.objects.filter(question=question)

    return render(request, "questions/index.html", {
        'question': question,
        'answers': answers,
        'form': form
    })

def ask(request):
    if request.method == "POST":
        form = AskForm(request.POST)
        form._user = request.user
        if form.is_valid():
            question = form.save()
            url = question.get_url()
            return HttpResponseRedirect(url)
    else:
        form = AskForm()
    return render(request, 'questions/ask.html', {
        'form': form
    })

def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return HttpResponseRedirect("/")
    else:
        form = SignupForm()
    return render(request, 'signup.html', {
        'form': form
    })

def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return HttpResponseRedirect("/")
    else:
        form = LoginForm()
    return render(request, 'login.html', {
        'form': form
    })
