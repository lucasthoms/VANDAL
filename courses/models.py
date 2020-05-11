from django.db import models
from django.core.exceptions import ValidationError

def validate_student_id(value):
   if str(value[0]).lower() != 'v':
      raise ValidationError('Student ID number does not begin with V')
   elif len(value) != 9:
      raise ValidationError('Student ID number is not 9 characters long')

def validate_semester(value):
   if str(value[0]).lower() not in ['f','s','u']:
      raise ValidationError('Semester name is not valid')
   elif not value[-2:].isdigit():
      raise ValidationError('Semester year is not valid')

class Course(models.Model):
   course_id = models.CharField(max_length=16,primary_key=True)
   course_name = models.CharField(max_length=64)
   credits = models.IntegerField()
   def __str__(self):
      return self.course_id

class Prereq(models.Model):
   course_id = models.ForeignKey(Course, models.PROTECT)
   prereq_id = models.ForeignKey(Course, models.PROTECT,related_name='prereq_course')
   coreq = models.BooleanField()
   def __str__(self):
      return f'{self.course_id} requires {self.prereq_id}{" as a coreq" if self.coreq else ""}'

class Requirement(models.Model):
   degree_type = models.CharField(max_length=6)
   major_name = models.CharField(max_length=64)
   course_rgx = models.CharField(max_length=128)
   description = models.CharField(max_length=128)
   credits = models.IntegerField()
   def __str__(self):
      return self.text()
   def text(self):
      if len(self.description) > 0:
         return self.description
      else:
         return self.course_rgx

class Student(models.Model):
   student_id = models.CharField(max_length=9,primary_key=True,validators=[validate_student_id])
   first_name = models.CharField(max_length=32)
   last_name = models.CharField(max_length=32)
   degree_type = models.CharField(max_length=6)
   major_name = models.CharField(max_length=64)
   grad_date = models.CharField(max_length=3,validators=[validate_semester])
   def __str__(self):
      return '{} {}'.format(self.first_name, self.last_name)

class Taken(models.Model):
   student_id = models.ForeignKey(Student, models.CASCADE)
   course_id = models.ForeignKey(Course, models.PROTECT)
   semester = models.CharField(max_length=3,validators=[validate_semester])
   grade = models.CharField(max_length=1,
      choices=[('A','A'),('B','B'),('C','C'),('D','D'),('F','F/Fail'),('P','Pass')]
   )
   def __str__(self):
      return str(f'{self.student_id}: {self.course_id}')
   def passed(self):
      return self.grade not in ['D','F']