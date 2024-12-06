from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import random
from . import models

users = User.objects.all()
def user_login(request):
    dic = {}
    if request.method == "POST":
        uname = request.POST['uname'].upper()
        password = request.POST['password']
        user = authenticate(username = uname, password = password )
        if models.fraud_model.objects.filter(username=uname).exists():
            return redirect('fraud')
        else:
            if user is not None :
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
            values['passerr'] = "password and confirm password doesn't match"

        else:
            userobj = User.objects.create_user(
                username=uname,
                password=pass1,
                first_name=fname,
                email=email
            )
            userobj.save()
            values["success"] = "Registration success"

            # return redirect('login')
    return render(request, "register.html", values)


def user_logout(request):
    logout(request)
    return redirect('home')


@login_required
def home(request):
    user = request.user
    
    if request.method == 'GET':
        # Get all subjects
        subjects = models.Subject.objects.all()
        return render(request, 'subject_selection.html', {'subjects': subjects})
    
    if request.method == 'POST':
        subject_id = request.POST.get('subject')
        
        # Check if user has already taken exam for this subject
        existing_score = models.leaderboard.objects.filter(
            username=user.username, 
            subject_id=subject_id
        ).exists()
        
        if existing_score:
            return HttpResponse("You have already completed this subject's exam")
        
        # Get questions for the selected subject
        questions = models.question.objects.filter(subject_id=subject_id)
        
        # Randomly select 4 questions
        l = [i for i in range(1, 5)]
        random.shuffle(l)
        
        context = {
            'questions': questions,
            'range': range(len(questions)),
            'l': l,
            'subject_id': subject_id
        }
        
        return render(request, 'home.html', context)

@login_required
def submit_exam(request):
    if request.method == 'POST':
        user = request.user
        subject_id = request.POST.get('subject_id')
        count = 0
        
        # Get all questions for the subject
        questions = models.question.objects.filter(subject_id=subject_id)
        
        # Create a list of question numbers
        l = [i for i in range(1, 5)]
        
        for i in l:
            selected_option = request.POST.get(f'question_{i}')
            correct_options = questions.filter(qno=i).values_list('co', flat=True)
            
            if selected_option in correct_options:
                count += 1
        
        # Create leaderboard entry
        scrobj = models.leaderboard.objects.create(
            username=user.username,
            subject_id=subject_id,
            score=count
        )
        
        return HttpResponse("Your exam is completed")
    
    
@login_required
def leaderboard(request):

    leaderboard_entries = models.leaderboard.objects.all().order_by('-score')[:10]
    return render(request, 'leaderboard.html', {'leaderboard_entries': leaderboard_entries})
from django.shortcuts import render




def fraud(request):
    uname = request.user
    if models.fraud_model.objects.filter(username=uname).exists():
            return render(request, 'fraud.html')
    elif uname is not None:
        fraud_user = models.fraud_model.objects.create(
            username = uname.username,
            fraud = True
        )
        fraud_user.save()
        logout(request)
        # return redirect('login')
    return render(request, 'fraud.html')


