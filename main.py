import os
import django
import random
import string

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quiz.settings')
django.setup()

from quizapp.models import Subject, question, leaderboard, fraud_model

def generate_random_string(length=10):
    return ''.join(random.choices(string.ascii_lowercase, k=length))

def populate_database():
    subjects = [
        'Mathematics', 'Physics', 'Chemistry', 'Biology', 
        'Computer Science', 'History', 'Geography', 'Literature'
    ]
    
    # Очистка существующих данных
    Subject.objects.all().delete()
    question.objects.all().delete()
    leaderboard.objects.all().delete()
    fraud_model.objects.all().delete()
    
    subject_objects = []
    for subject_name in subjects:
        subject_obj = Subject.objects.create(name=subject_name)
        subject_objects.append(subject_obj)
    
    # Создание вопросов
    for _ in range(50):
        subject = random.choice(subject_objects)
        question.objects.create(
            subject=subject,
            qno=random.randint(1, 100),
            question=f"Случайный вопрос по {subject.name}?",
            o1=generate_random_string(),
            o2=generate_random_string(),
            o3=generate_random_string(),
            o4=generate_random_string(),
            co=generate_random_string()
        )
    
    # Создание записей в leaderboard
    usernames = [generate_random_string() for _ in range(50)]
    for username in usernames:
        leaderboard.objects.create(
            username=username,
            subject=random.choice(subject_objects),
            score=random.randint(0, 100)
        )
    
    # Создание записей в fraud_model
    for username in usernames[:10]:  # 10 случайных пользователей помечаем как мошенников
        fraud_model.objects.create(
            username=username,
            fraud=random.choice([True, False])
        )
    
    print("База данных успешно заполнена!")

if __name__ == '__main__':
    populate_database()