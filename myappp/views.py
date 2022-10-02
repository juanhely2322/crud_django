
import re
from django.http import HttpResponse
from django.shortcuts import render, redirect,get_object_or_404
# trae formulario de registro o signup
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
# con esta funsion se puede crear una cookie para manter la secion aciva
# login= crea cookie para mantener inicio de sesion
from django.contrib.auth import login, logout, authenticate
# logut= sirve para cerrar la secion
# authenticate= sirve para verificar que el usuario exista y la contraseña este correcta e iniciar secion
from django.db import IntegrityError
from .forms import CreateTaskForm
from .models import task
from django.utils import timezone
from django.contrib.auth.decorators import login_required


# Create your views here.
def home(request):

    return render(request, "home.html")


def signup(request):
    if request.method == 'GET':
        return render(request, "singup.html", {'form': UserCreationForm})
    else:
        if request.POST["password1"] == request.POST["password2"]:
            # register user
            try:
                user = User.objects.create_user(
                    username=request.POST["username"], password=request.POST["password1"])
                user.save()

                login(request, user)

                return redirect("tasks")
            except IntegrityError:
                return render(request, "singup.html", {'form': UserCreationForm, "error": "User already exist "})
        else:
            return render(request, "singup.html", {'form': UserCreationForm, "error": "Password do not match"})

@login_required
def tasks(request):
    tasks = task.objects.filter(user=request.user,datecomplete__isnull=True)
    return (render(request, "tasks.html",{"tasks":tasks,"estute":"Incompleted"}))
@login_required
def task_completed(request):
    tasks = task.objects.filter(user=request.user,datecomplete__isnull=False).order_by("-datecomplete")
    return render(request,"tasks.html",{"tasks":tasks,"estute":"Completed"})
@login_required
def create_task(request):
    if request.method == "GET":
        return render(request, "created_task.html", {
            "form": CreateTaskForm,
        })
    else:
        try:
            form = CreateTaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect("tasks")
        
        except ValueError:
                 return render(request, "created_task.html", {
                "error":"please provide valide data",
 
                     })


#listar tarea individual
@login_required    
def task_detail(request,task_id):
    if request.method=="GET":
        tasks=get_object_or_404(task,pk=task_id,user=request.user)
        form = CreateTaskForm(instance=tasks)
        return render(request,("task_detail.html"),{"tasks":tasks, "form":form})
    else:
        try:
            tasks=get_object_or_404(task,pk=task_id,user=request.user)
            form=CreateTaskForm(request.POST,instance=tasks)
            form.save()
            return redirect("tasks")
        except ValueError:
            return render(request,("task_detail.html"),{"tasks":tasks, "form":form, "error":"Error updating task"})

@login_required
def complete_task(request,task_id):
    tasks=get_object_or_404(task, pk=task_id, user=request.user)
    if  request.method=="POST":
        tasks.datecomplete = timezone.now()
        tasks.save()
        #print(tasks.save())
        return redirect("tasks")
@login_required   
def delete_task(request,task_id):
    tasks=get_object_or_404(task, pk=task_id, user=request.user)
    if  request.method=="POST":
        tasks.delete()
        return redirect("tasks")
         
    
    

# cerrar session
@login_required
def logout_session(request):
    logout(request)
    return redirect("home")
# inicio sesion


def login_session(request):
    if request.method == "GET":
        return render(request, "login.html", {"form": AuthenticationForm})
    else:
        user = authenticate(
            request, username=request.POST["username"], password=request.POST["password"])
        if user is None:
            return render(request, "login.html", {"form": AuthenticationForm,
                                                  "error": "Username o password is incorrect"})
        else:
            login(request, user)
            return redirect("tasks")
