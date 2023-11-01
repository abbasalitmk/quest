from django.shortcuts import render, redirect
from .models import Question, Answer, Like
from .forms import QuestionForm, AnswerForm
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponse


@login_required(login_url='login')
def home(request):
    error = ""
    try:
        questions = Question.objects.all().order_by('-updated_at')[:10]
    except Question.DoesNotExist:
        error = "No questions found!"

    context = {
        "questions": questions,
        "error": error
    }

    return render(request, "index.html", context)


@login_required(login_url='login')
def create_question(request):
    form = QuestionForm()
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            question = form.save()
            return redirect('home')
        else:
            form = QuestionForm()

    return render(request, 'posts/ask.html', {"form": form})


@login_required(login_url='login')
def show_question(request, question_id):
    form = AnswerForm()

    question = get_object_or_404(Question, id=question_id)
    answers = Answer.objects.filter(
        question=question).order_by('-updated_at')[:10]

    like_status = False
    try:
        Like.objects.get(answer__in=answers, user=request.user)
        like_status = True
    except Like.DoesNotExist:
        like_status = False

    context = {
        "form": form,
        "question": question,
        "user": question.user,
        "like_status": like_status,
        "answer": answers
    }

    return render(request, 'posts/question.html', context)


@login_required(login_url='login')
def answer_question(request, question_id):
    form = AnswerForm()
    question = Question.objects.get(id=question_id)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.user = request.user
            answer.question = question
            answer.save()
            return redirect('question', question_id=question_id)
        else:
            form = form = AnswerForm()
    return render(request, 'posts/answer.html', {"form": form, "question": question})


@login_required(login_url='login')
def like(request, answer_id):
    try:
        answer = Answer.objects.get(id=answer_id)

        if request.user in answer.likes.all():
            answer.likes.remove(request.user)
            messages.success(request, 'Unliked successfully')
        else:
            answer.likes.add(request.user)
            messages.success(request, 'Liked successfully')

        question_url = reverse('question', kwargs={
                               'question_id': answer.question.id})
        return redirect(question_url)
    except Exception as e:
        messages.error(request, str(e))
        return HttpResponse(str(e))
