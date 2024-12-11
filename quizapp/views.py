from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import random
from . import models

def user_login(request):
    dic = {}
    if request.method == "POST":
        uname = request.POST['uname'].upper()
        password = request.POST['password']
        user = authenticate(username=uname, password=password)
        if models.FraudModel.objects.filter(user__username=uname).exists():
            return redirect('fraud')
        else:
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                dic['warning'] = "Fake Login credentials"
    return render(request, "login.html", dic)

def register(request):
    values = {}
    if request.method == "POST":
        fname = request.POST['fname']
        pass1 = request.POST['password']
        pass2 = request.POST['confirmpassword']
        uname = request.POST['uname'].upper()
        email = request.POST['email']
        if User.objects.filter(username=uname).exists():
            values['exists'] = "Roll No already exists."
            values['fname'] = fname
            values['uname'] = uname
        elif uname == "":
            values['fname'] = fname
            values['uname'] = uname
            values['exists'] = "Rollno is empty"
        elif fname == "":
            values['fname'] = fname
            values['uname'] = uname
            values['teamerr'] = "Team Name is empty"
        elif pass1 == "":
            values['fname'] = fname
            values['uname'] = uname
            values['passerr'] = "Password is empty"
        elif email == "":
            values['fname'] = fname
            values['uname'] = uname
            values['emailerr'] = "Email is empty"
        elif pass1 != pass2:
            values['fname'] = fname
            values['uname'] = uname
            values['passerr'] = "Password and confirm password don't match"
        else:
            userobj = User.objects.create_user(
                username=uname,
                password=pass1,
                first_name=fname,
                email=email
            )
            userobj.save()
            # Автоматическое создание записи FraudModel при регистрации
            models.FraudModel.objects.create(user=userobj)
            values["success"] = "Registration successful"
            # return redirect('login')
    return render(request, "register.html", values)

def user_logout(request):
    logout(request)
    return redirect('home')

@login_required
def home(request):
    user = request.user
    
    if request.method == 'GET':
        subjects = models.Subject.objects.all()
        return render(request, 'subject_selection.html', {'subjects': subjects})
    
    if request.method == 'POST':
        subject_id = request.POST.get('subject')
        print(f"Selected subject_id: {subject_id}")  # Отладка
        
        existing_score = models.Leaderboard.objects.filter(
            user=user, 
            subject_id=subject_id
        ).exists()
        
        if existing_score:
            return HttpResponse("You have already completed this subject's exam")
        
        # Получение вопросов для выбранного предмета
        questions = models.Question.objects.filter(subject_id=subject_id)
        print(f"Number of questions: {questions.count()}")  # Отладка
        
        if not questions.exists():
            return HttpResponse("No questions available for this subject")
        
        # Выбор 4 случайных вопросов
        selected_questions = random.sample(list(questions), min(4, questions.count()))
        
        context = {
            'questions': selected_questions,
            'subject_id': subject_id
        }
        
        return render(request, 'home.html', context)

@login_required
def submit_exam(request):
    if request.method == 'POST':
        user = request.user
        subject_id = request.POST.get('subject_id')
        
        # Check if the user has already taken the exam for this subject
        existing_entry = models.Leaderboard.objects.filter(
            user=user, 
            subject_id=subject_id
        ).first()
        
        if existing_entry:
            return HttpResponse("You have already completed this subject's exam")
        
        # Rest of your existing code remains the same
        count = 0
        
        # Получение всех вопросов для предмета
        questions = models.Question.objects.filter(subject_id=subject_id)
        
        # Создание списка номеров вопросов
        qnos = [q.qno for q in questions]
        
        for qno in qnos:
            selected_option = request.POST.get(f'question_{qno}')
            correct_options = questions.filter(qno=qno).values_list('co', flat=True)
            
            print(f"Question {qno}: Selected option: {selected_option}, Correct option: {list(correct_options)}")  # Отладка
            
            if selected_option in correct_options:
                count += 1
        
        # Создание записи в Leaderboard
        scrobj = models.Leaderboard.objects.create(
            user=user,
            subject_id=subject_id,
            score=count
        )
        
        print(f"User {user.username} scored {count} in subject {subject_id}")  # Отладка
        
        return HttpResponse("Your exam is completed")
@login_required
def leaderboard_view(request):
    leaderboard_entries = models.Leaderboard.objects.all().order_by('-score')[:10]
    return render(request, 'leaderboard.html', {'leaderboard_entries': leaderboard_entries})

def fraud(request):
    if request.user.is_authenticated and models.FraudModel.objects.filter(user=request.user).exists():
        return render(request, 'fraud.html')
    elif request.user.is_authenticated:
        # Если пользователь аутентифицирован, но запись FraudModel отсутствует, создаём её
        fraud_user = models.FraudModel.objects.create(
            user=request.user,
            fraud=True
        )
        fraud_user.save()
        logout(request)
        # return redirect('login')
    return render(request, 'fraud.html')
