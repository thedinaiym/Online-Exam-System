# quizapp/models.py

from django.db import models
from django.contrib.auth.models import User

class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name

class Question(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    qno = models.IntegerField()
    question = models.CharField(max_length=255)
    o1 = models.CharField(max_length=255)
    o2 = models.CharField(max_length=255)
    o3 = models.CharField(max_length=255)
    o4 = models.CharField(max_length=255)
    co = models.CharField(max_length=255)  # Правильный ответ
    
    def __str__(self):
        return f"{self.subject.name} - {self.question}"
class Leaderboard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True)
    score = models.IntegerField()
    
    class Meta:
        unique_together = ('user', 'subject')  # Обеспечивает уникальность записи для пользователя и предмета
    
    def __str__(self):
        return f"{self.user.username} - {self.subject.name if self.subject else 'No Subject'}"
class FraudModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fraud = models.BooleanField(default=False)
    
    def __str__(self):
        return self.user.username
