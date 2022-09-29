from django.urls import URLPattern, path

from . import views


urlpatterns=[
    path("",views.home,name="home"),
    path("signup",views.signup,name="signup"),
    path("tasks",views.tasks,name="tasks"),
    path("tasks/create",views.create_task,name="create_task"),
    path("logout",views.logout_session,name="logout"),
    path("login",views.login_session,name="login"),
    
]