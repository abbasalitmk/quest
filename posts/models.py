from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Question(models.Model):
    title = models.CharField(max_length=255)
    user = models.ForeignKey(
        User, related_name="questions", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Answer(models.Model):
    question = models.ForeignKey(
        Question, related_name="answer", on_delete=models.CASCADE
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(
        User, related_name="liked_answers", blank=True)

    def __str__(self):
        return self.question.title


class Like(models.Model):
    answer = models.ForeignKey(
        Answer, related_name='like', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="like",
                             on_delete=models.CASCADE)
