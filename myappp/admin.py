from django.contrib import admin
from .models import task

class TaskAdmin(admin.ModelAdmin):# se usa la clase para heredar 
     readonly_fields=("created",)#se susa para mostrar los campos de solo lectura en el admin de django
# Register your models here.

admin.site.register(task,TaskAdmin)