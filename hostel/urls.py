from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('get',views.view_students,name='view_student'),
    path('add',views.add_student,name='add_student'),
    path('edit/<int:student_id>',views.edit_student,name='edit_student'),
    path('delete/<int:student_id>',views.delete_student,name='delete_student'),
    path('allot',views.allot_student,name='allot_student'),
    path('allotements',views.view_allotement,name='view_allotement'),

]