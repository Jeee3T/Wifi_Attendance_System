from django.contrib import admin
from .models import *


class adminClass(admin.ModelAdmin):
    list_display = ['name', 'returnList']
    
    def returnList(self, instance):
        if instance.students.all():
            return list(instance.students.values_list())

class adminStudent(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'roll_number', 'returnList']

    def returnList(self, instance):
        if instance._classes.all():
            return list(instance._classes.all().values_list())

class Router(admin.ModelAdmin):
    def returnValue():
        return ['id', 'mac_address']
    
    returnValue()

admin.site.register(Class, adminClass)
admin.site.register(Student, adminStudent)
admin.site.register(WifiRouter, Router)