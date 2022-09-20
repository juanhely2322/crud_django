from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


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

                return render(request, "singup.html", {'form': UserCreationForm, "error": "User create successfully"})
            except:
                return render(request, "singup.html", {'form': UserCreationForm, "error": "User already exist "})
        else:
            return render(request, "singup.html", {'form': UserCreationForm, "error": "Password do not match"})
