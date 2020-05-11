from django.urls import path

from . import views

urlpatterns = [
   path('', views.index, name='index'),
   path('all/', views.course_list, name='course_list'),
   path('<str:student_id>/reqs/', views.requirement_list, name='requirement_list'),
   #path('0/reqs/', views.requirement_list, name='all_requirement_list')
]