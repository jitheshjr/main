from django.shortcuts import redirect,render
from django.http import HttpResponse
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from datetime import timedelta,datetime,date
from django.contrib import messages
# Create your views here.

@login_required()
def home(request):
    return render(request,'hostel/home.html')

#adding student to Student model
@login_required()
def add_student(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view_student')
    else:
        form = StudentForm()
    return render(request,'hostel/add_stud.html',{'form':form})

#fetching data from Student model
@login_required()
def view_students(request):
    stud = Student.objects.select_related('pgm_id').all().order_by('pgm_id')
    return render(request,'hostel/students.html',{'stud':stud})

#editing existing data in Student model
@login_required()
def edit_student(request,student_id):
    student = Student.objects.get(id=student_id)
    form = StudentForm(instance=student)

    if request.method == "POST":
        form = StudentForm(request.POST,instance=student)
        if form.is_valid():
            form.save()
            return redirect('view_student')
    return render(request,'hostel/edit.html',{'form':form})

#deleting existing data from Student model
@login_required()
def delete_student(request,student_id):
    if request.method == 'GET':
        student = Student.objects.get(id=student_id)
        student.delete()
        return redirect('view_student')
    else:
        return HttpResponse("ERROR OCCURED")



#room allotement of student 
@login_required()
def allot_student(request):
    if request.method == "POST":
        form = AllotementForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view_allotement')
    else:
        form = AllotementForm()
    return render(request,'hostel/allot_stud.html',{'form':form})

#edit allocated room
@login_required()
def edit_allocation(request,student_name):

    Alloted_object = Allotment.objects.get(name__name=student_name)
    #name is a OneToOneField to the Student model. The double underscore is used to access fields within related models.
    alloc_form = AllotementForm(instance=Alloted_object)

    if request.method == "POST":
        alloc_form = AllotementForm(request.POST,instance=Alloted_object)
        if alloc_form.is_valid():
            alloc_form.save()
            return redirect('view_allotement')
    return render(request,'hostel/edit_allocation.html',{'form':alloc_form})

#delete allocated room
@login_required()
def delete_allocation(request,student_name):
    if request.method == "GET":
        allot_obj = Allotment.objects.get(name__name=student_name)
        allot_obj.delete()
        return redirect('view_allotement')
    else:
        return HttpResponse("Error Occured")

#fetching data from Allotement model
@login_required()
def view_allotement(request):
    alloted_list = Allotment.objects.select_related('room_number','name').all().order_by('room_number')
    return render(request,'hostel/allotements.html',{'alloted':alloted_list})



#marking attendance
@login_required()
def mark_attendance(request):
    today = date.today()  # Get today's date
    if request.method == "POST":
        names = request.POST.getlist('name')
        today = request.POST.get('date')
        repeated_attendance = False  # Flag to track if there are repeated attendances
        for name in names:
            student = Student.objects.get(name=name)
            # Check if attendance already exists for this student on the given date
            if Attendance.objects.filter(name=student, dates=today).exists():
                # If attendance exists, add an error message for this repeated attendance
                messages.error(request, f"Attendance for {name} on {today} already exists.")
                repeated_attendance = True
        if repeated_attendance:
            return redirect('mark_attendance')
        else:
            for name in names:
                student = Student.objects.get(name=name)
                attendance = Attendance(name=student, dates=today)
                attendance.save()
            return redirect('view_attendance')

    att = {
        'attendance': Student.objects.all(),
        'today': today.strftime('%Y-%m-%d')  # Format today's date as a string
    }
    return render(request, 'hostel/attendance.html', att)

#fetching attendance data
@login_required()
def view_attendance(request):
    attendance_list = Attendance.objects.all().select_related('name')
    return render(request,"hostel/summary.html",{'summary':attendance_list})

# Define a function to calculate consecutive absences
def calculate_consecutive_absences(request):
    if request.method == 'POST':
        form = DateRangeForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']

            # Calculate the end date of the current month
            end_of_current_month = end_date + timedelta(days=1)

        # Query attendance records within the specified date range
        attendance_records = Attendance.objects.filter(
            dates__gte=start_date,
            dates__lt=end_of_current_month
        ).order_by('name_id', 'dates').values('name_id', 'dates')

        current_name_id = None
        consecutive_absences_count = 0
        consecutive_absences = []

        # Iterate over attendance records to find consecutive absences
        for record in attendance_records:
            if record['name_id'] == current_name_id:
                if record['dates'] == previous_date + timedelta(days=1):
                    consecutive_absences_count += 1
                else:
                    if consecutive_absences_count >= 7:
                        consecutive_absences.append({'name_id': current_name_id, 'consecutive_absences': consecutive_absences_count})
                    consecutive_absences_count = 1
            else:
                if consecutive_absences_count >= 7:
                    consecutive_absences.append({'name_id': current_name_id, 'consecutive_absences': consecutive_absences_count})
                consecutive_absences_count = 1

            current_name_id = record['name_id']
            previous_date = record['dates']

        if consecutive_absences_count >= 7:
            consecutive_absences.append({'name_id': current_name_id, 'consecutive_absences': consecutive_absences_count})
        
        # Prepare context data to pass to the template
        context = {
            'consecutive_absences': consecutive_absences
        }
    else:
        form = DateRangeForm()
        context = {}
    
    context.update({'form':form})
    
    return render(request, "hostel/reduction.html", context)
