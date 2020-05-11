from django.contrib import admin

from .models import Course, Prereq, Requirement, Student, Taken

admin.site.register(Course)
admin.site.register(Prereq)
admin.site.register(Requirement)
admin.site.register(Student)
admin.site.register(Taken)