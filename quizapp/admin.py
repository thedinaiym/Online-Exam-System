# quizapp/admin.py

from django.contrib import admin
from .models import Question, FraudModel, Leaderboard, Subject

admin.site.register(Question)
admin.site.register(FraudModel)
admin.site.register(Leaderboard)
admin.site.register(Subject)
