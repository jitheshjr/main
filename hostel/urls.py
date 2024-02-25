from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('get/',views.view_students,name='view_student'),
    path('add/',views.add_student,name='add_student'),
    path('view/<int:student_id>/',views.view_details,name='view_details'),
    path('edit_student/<int:student_id>/',views.edit_student,name='edit_student'),
    path('delete_student/<int:student_id>/',views.delete_student,name='delete_student'),
    path('allot/',views.allot_student,name='allot_student'),
    path('allotements/',views.view_allotement,name='view_allotement'),
    path('attendance/',views.mark_attendance,name='mark_attendance'),
    path('summary/',views.view_attendance,name='view_attendance'),
    path('edit_allocation/<str:student_name>/',views.edit_allocation,name='edit_allocation'),
    path('delete_allocation/<str:student_name>/',views.delete_allocation,name='delete_allocation'),
    path('absences',views.calculate_consecutive_absences,name='calculate_consecutive_absences'),
    path('messbill',views.generate_mess_bill,name='generate_mess_bill'),
    path('viewbill',views.view_bill,name='view_bill'),
    path('monthlybills',views.view_monthly_bill,name='view_monthly_bill')
]