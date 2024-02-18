from django import forms
from .models import *


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
    
class AllotementForm(forms.ModelForm):
    class Meta:
        model = Allotment
        fields = '__all__'

class BillForm(forms.Form):
    start_date = forms.DateField(label='Start Date', widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(label='End Date', widget=forms.DateInput(attrs={'type': 'date'}))
    number_of_students = forms.IntegerField(label='Total Students', min_value=0)
    total_mess_amount = forms.DecimalField(label='Amount', min_value=0)
    room_rent = forms.DecimalField(label='Room Rent', min_value=0)
    staff_salary = forms.DecimalField(label='Staff Salary', min_value=0)
    electricity_bill = forms.DecimalField(label='Electricity Bill', min_value=0)
