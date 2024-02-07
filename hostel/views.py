from django.shortcuts import render,redirect
from .models import *
from .forms import *
from django.http import HttpResponse
# Create your views here.

def home(request):
    return render(request,'hostel/home.html')

#fetching data from Student model
def view_students(request):
    stud = Student.objects.select_related('pgm_id').all().order_by('pgm_id')
    return render(request,'hostel/students.html',{'stud':stud})


#adding student to Student model
def add_student(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view_student')
    else:
        form = StudentForm()
    return render(request,'hostel/add_stud.html',{'form':form})


def edit_student(request,student_id):
    student = Student.objects.get(id=student_id)
    form = StudentForm(instance=student)

    if request.method == "POST":
        form = StudentForm(request.POST,instance=student)
        if form.is_valid():
            form.save()
            return redirect('view_student')
    return render(request,'hostel/edit.html',{'form':form})


def delete_student(request,student_id):
    if request.method == 'GET':
        student = Student.objects.get(id=student_id)
        student.delete()
        return redirect('view_student')
    else:
        return HttpResponse("ERROR OCCURED")

#room allotement of student 
def allot_student(request):
    if request.method == "POST":
        form = AllotementForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view_allotement')
    else:
        form = AllotementForm()
    return render(request,'hostel/allot_stud.html',{'form':form})

#fetching data from Allotement model
def view_allotement(request):
    alloted_list = Allotment.objects.select_related('room_number','name').all().order_by('room_number')
    return render(request,'hostel/allotements.html',{'alloted':alloted_list})

#marking attendance
def mark_attendance(request):
    if request.method == "POST":
        names = request.POST.getlist('name')
        date = request.POST.get('date')
        print(names)
        print(date)
        for name in names:
            attendance = Attendance(name=name,date=date)
            attendance.save()
        return redirect('view_student')
    att={
        'attendance':Student.objects.all()
    }
    return render(request,'hostel/attendance.html',att)

def view_attendance(request):
    summary = {
        'attendance':Attendance.objects.all()
    }
    return render(request,"hostel/summary.html",summary)