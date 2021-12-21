from django.db import models


class Topic(models.Model):
    name = models.CharField(max_length=500)


class Question(models.Model):
    text = models.TextField()
    type = models.CharField(max_length=30)
    topic = models.ForeignKey(to=Topic, on_delete=models.deletion.CASCADE)


class Answer(models.Model):
    right = models.BooleanField(default=False)
    text = models.TextField()
    question = models.ForeignKey(to=Question, on_delete=models.deletion.CASCADE, related_name='answers')

