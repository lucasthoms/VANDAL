from django.shortcuts import render
from django.db.models import Sum

from .models import *

def course_list(request):
   all_course_list = Course.objects.all()
   context = {
      'all_course_list': all_course_list,
   }
   return render(request, 'courses/course_list.html', context)

def requirement_list(request, student_id=0):
   all_requirements_list = Requirement.objects.all()
   closed_requirements_list, open_requirements_list = [], []
   unsatisfied_prereqs = Prereq.objects.raw('SELECT * FROM courses_prereq WHERE prereq_id_id NOT IN (SELECT course_id_id FROM courses_taken WHERE student_id_id = %s)',[student_id])
   unsatisfied_prereq_list = []
   for prereq in unsatisfied_prereqs:
      unsatisfied_prereq_list.append(prereq.course_id_id)
   used_courses = []
   for req in all_requirements_list:
      taken_creds = 0
      match_dict = {}
      sugg_dict = {}
      matches = Taken.objects.raw('SELECT * FROM courses_taken WHERE course_id_id REGEXP %(course)s AND student_id_id = %(student)s;',{'course': req.course_rgx, 'student': student_id})
      for match in matches:
         course = match.course_id
         if course not in used_courses:
            taken_creds += course.credits
            match_dict[course.course_id] = course.course_name
            used_courses.append(course)
      if taken_creds >= req.credits:
         closed_requirements_list.append((req.text(), match_dict, taken_creds, req.credits))
      else:
         matches = Course.objects.raw('SELECT * FROM courses_course WHERE course_id REGEXP %s;',[req.course_rgx])
         for match in matches:
            if match not in used_courses:
               if match.course_id in unsatisfied_prereq_list:
                  sugg_dict[match.course_id] = "*"+match.course_name
               else:
                  sugg_dict[match.course_id] = match.course_name
         open_requirements_list.append((req.text(), match_dict, sugg_dict, taken_creds, req.credits))

   try:
      student = Student.objects.get(student_id=student_id)
      student_details = {'name': f'{student.first_name} {student.last_name}', 'degree': f'{student.degree_type} in {student.major_name}'}
   except Student.DoesNotExist:
      student_details = {'name': '0', 'degree': ''}

   context = {
      'student_details': student_details,
      'open_requirements_list': open_requirements_list,
      'closed_requirements_list': closed_requirements_list,
   }
   return render(request, 'courses/requirement_list.html', context)

def index(request):
   students = Student.objects.all()

   requirements = Requirement.objects.all()

   degrees = set([])

   for req in requirements:
      degrees.add((req.degree_type, req.major_name))

   context = {
      'student_list': students,
      'degree_list': degrees,
   }
   return render(request, 'courses/student_list.html', context)