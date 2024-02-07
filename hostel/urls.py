from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('get',views.view_students,name='view_student'),
    path('add',views.add_student,name='add_student'),
    path('edit_student/<int:student_id>',views.edit_student,name='edit_student'),
    path('delete_student/<int:student_id>',views.delete_student,name='delete_student'),
    path('allot',views.allot_student,name='allot_student'),
    path('allotements',views.view_allotement,name='view_allotement'),
    path('attendance',views.mark_attendance,name='mark_attendance'),
    path('summary',views.view_attendance,name='view_attendance'),
    path('edit_allocation/<int:room_number>',views.edit_allocation,name='edit_allocation'),
    path('delete_allocation/<int:room_number>',views.delete_allocation,name='delete_allocation'),
]