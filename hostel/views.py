from django.shortcuts import redirect,render
from django.http import HttpResponse
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from datetime import timedelta,date
from django.contrib import messages
from decimal import Decimal
from django.core.files.storage import default_storage
from django.conf import settings
# Create your views here.

@login_required()
def home(request):
    return render(request,'hostel/home.html')



# Student manipulating functions

@login_required()
def add_student(request):
    if request.method == "POST":
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('view_student')
    else:
        form = StudentForm()
    return render(request,'hostel/add_stud.html',{'form':form})

@login_required()
def view_students(request):
    stud = Student.objects.select_related('pgm').all().order_by('pgm')
    return render(request,'hostel/students.html',{'stud':stud})

def view_details(request, student_id):
    student = Student.objects.filter(id=student_id).select_related('pgm').first()
    room = Allotment.objects.filter(name_id=student_id).select_related('room_number').first()
    student_image_url = None
    if student and student.photo:
        student_image_url = settings.MEDIA_URL + str(student.photo)
    return render(request, "hostel/details.html", {'student': student, 'student_image_url': student_image_url,'room':room})

@login_required()
def edit_student(request, student_id):
    student = Student.objects.get(id=student_id)
    form = StudentForm(instance=student)

    if request.method == "POST":
        form = StudentForm(request.POST, request.FILES, instance=student)  # Include request.FILES to handle file uploads
        if form.is_valid():
            # Check if the image field has changed
            if 'image' in form.changed_data:
                # Delete old image file if it exists
                if student.image:
                    default_storage.delete(student.image.path)
            
            # Save form data including the image field
            student = form.save()

            return redirect('view_student')
    
    return render(request, 'hostel/edit.html', {'form': form})


@login_required()
def delete_student(request,student_id):
    if request.method == 'GET':
        student = Student.objects.get(id=student_id)
        student.delete()
        return redirect('view_student')
    else:
        return HttpResponse("ERROR OCCURED")

# Room allocation functions

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

@login_required()
def delete_allocation(request,student_name):
    if request.method == "GET":
        allot_obj = Allotment.objects.get(name__name=student_name)
        allot_obj.delete()
        return redirect('view_allotement')
    else:
        return HttpResponse("Error Occured")

@login_required()
def view_allotement(request):
    alloted_list = Allotment.objects.select_related('room_number','name').all().order_by('room_number')
    return render(request,'hostel/allotements.html',{'alloted':alloted_list})



# Attendance functions

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

@login_required()
def view_attendance(request):
    attendance_list = Attendance.objects.all().select_related('name')  #.order_by('name')
    return render(request,"hostel/summary.html",{'summary':attendance_list})



# mess bill functions

@login_required()
def calculate_consecutive_absences(request):
    if request.method == 'POST':
        form = BillForm(request.POST)
        if form.is_valid():

            #storing data from the form 
            
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            number_of_students = form.cleaned_data['number_of_students']
            total_mess_amount = form.cleaned_data['total_mess_amount']
            room_rent = form.cleaned_data['room_rent']
            staff_salary = form.cleaned_data['staff_salary']
            electricity_bill = form.cleaned_data['electricity_bill']

            year = start_date.year
            month = start_date.strftime('%B')     #month as string
            
            mess_days = (end_date-start_date).days + 1     #calculating number of days
            

            session_items = {
                'month':month,
                'year':year,
                'mess_days':mess_days,
                'total_mess_amount':str(total_mess_amount),
                'number_of_students':number_of_students,
                'room_rent':str(room_rent),
                'staff_salary':str(staff_salary),
                'electricity_bill':str(electricity_bill)
            }
            
            request.session['session_items'] = session_items     #storing to session

            
            end_of_current_month = end_date + timedelta(days=1)     
            # Query attendance records within the specified date range
            
            attendance_records = Attendance.objects.filter(
                dates__gte=start_date,
                dates__lt=end_of_current_month
            ).select_related('name').order_by('name_id', 'dates').values('name_id', 'dates')

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
             
            context = {
                'consecutive_absences': consecutive_absences     
            }
            request.session['consecutive_absence'] = context     #storing continous absence details in session

            return redirect('generate_mess_bill')
        else:
            context = {'form': form}
    else:
        form = BillForm()
        context = {'form': form}
    return render(request, "hostel/billform.html", {'form': form})

@login_required()
def generate_mess_bill(request):

    details = request.session.get('session_items')     #retrieving data from session

    #initialising data from session

    month = details['month']
    mess_days = details['mess_days']
    amount = Decimal(details['total_mess_amount'])
    students = details['number_of_students']
    room_rent = Decimal(details['room_rent'])
    staff_salary = Decimal(details['staff_salary'])
    electricity_bill = Decimal(details['electricity_bill'])
    year = details['year']
    reduction_days = 0

    print(f"month: {month}")
    print(f"mess days: {mess_days}")
    print(f"Amount: {amount}")
    print(f"Students: {students}")
    print(f"Rent: {room_rent}")
    print(f"Salary: {staff_salary}")
    print(f"Electricity bill: {electricity_bill}")
    print(f"year: {year}")

    messbill = MessBill(no_of_students=students,month=month,mess_days=mess_days,mess_amount=amount,room_rent=room_rent,staff_salary=staff_salary,electricity_bill=electricity_bill,year=year)
    messbill.save()     #saving each months expenses into the database

    #Retrieve the consecutive absence data from the session

    consecutive_absence_dict = request.session.get('consecutive_absence')

    consecutive_absence_data = {}

    # Iterate over the consecutive absence data

    for item in consecutive_absence_dict.get('consecutive_absences', []):
        student_id = item['name_id']
        streak = item['consecutive_absences']
        reduction_days += streak
        
        # Update or add the streak for the student_id
        # consecutive_absence_data contains accumulated streaks for each student_id

        if student_id in consecutive_absence_data:
            consecutive_absence_data[student_id] += streak
        else:
            consecutive_absence_data[student_id] = streak


    total_mess_days = (students * mess_days) - reduction_days     #number of mess days after reducing reduction days
    print(f"total reduction days: {reduction_days}")
    print(f"Total mess days: {total_mess_days}")

    
    mess_bill_per_day = amount / total_mess_days     #per day charge for mess
    other_expenses_per_student = ((room_rent*students) + (staff_salary + electricity_bill)) / students     #other expences

    print(f"mess bill per day :{mess_bill_per_day}")
    print(f"other_expenses_per_student :{other_expenses_per_student}")

    total = 0
    students = Student.objects.all()     #retrieving all students from Student model

    for student in students:
        if student.id in consecutive_absence_data.keys():
            days_present = mess_days - consecutive_absence_data[student.id]
            mess_bill = round((mess_bill_per_day * days_present)+other_expenses_per_student,2)
            total += mess_bill

            student_bill = StudentBill(name=student,total=mess_bill,month=month,year=year) 
            student_bill.save()     #saving each students monthly bill to the database

            print(f"{student} present for {days_present}")
        else:
            days_present = mess_days
            mess_bill = round((mess_bill_per_day * days_present)+other_expenses_per_student ,2)
            total += mess_bill

            student_bill = StudentBill(name=student,total=mess_bill,month=month,year=year)
            student_bill.save()     #saving each students monthly bill to the database

            print(f"{student} present for {days_present}")
    print(f"total bill of hostel: {total}")
    
    return redirect('view_monthly_bill')

@login_required()
def view_bill(request):
    context = StudentBill.objects.all().select_related('name')
    return render(request,"hostel/bill.html",{'bills':context})

@login_required()
def view_monthly_bill(request):
    details = request.session.get('session_items')
    month = details.get('month')
    year = details.get('year')
    print(year)
    bills = StudentBill.objects.filter(month=month,year=year).select_related('name')
    return render(request,"hostel/month_bill.html",{'bills':bills})

