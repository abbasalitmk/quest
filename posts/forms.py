from django import forms
from .models import Question, Answer


class QuestionForm(forms.ModelForm):
    title = forms.CharField(label="Question", widget=forms.TextInput(
        attrs={'style': 'height: 4rem;'}))

    class Meta:
        model = Question
        fields = ['title']


class AnswerForm(forms.ModelForm):
    answer = forms.CharField(label="Your Answer", widget=forms.Textarea(
        attrs={'style': 'height: 8rem;'}))

    class Meta:
        model = Answer
        fields = ['answer']
