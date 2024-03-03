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
from django.http import Http404
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
    attendance_list = Attendance.objects.all().select_related('name').order_by('name')
    return render(request,"hostel/summary.html",{'summary':attendance_list})



# mess bill functions

@login_required()
def generate_mess_bill(request):
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
            month = start_date.strftime('%B')     #month as string\
            

            existing_bill = MessBill.objects.filter(month=month, year=year).exists()
            if existing_bill:
                error_message = f"A bill for {month}, {year} already exists"
                return render(request, "hostel/billform.html", {'form': form,'error_message':error_message})

            else:
                mess_days = (end_date-start_date).days + 1     #calculating number of days
                
                end_of_current_month = end_date + timedelta(days=1)     

                messbill = MessBill(no_of_students=number_of_students,month=month,mess_days=mess_days,mess_amount=total_mess_amount,room_rent=room_rent,staff_salary=staff_salary,electricity_bill=electricity_bill,year=year)
                messbill.save()

                # Query attendance records within the specified date range
                attendance_records = Attendance.objects.filter(
                    dates__gte=start_date,
                    dates__lt=end_of_current_month
                ).select_related('name').order_by('name_id', 'dates').values('name_id', 'dates')

                current_name_id = None
                consecutive_absences_count = 0

                # Iterate over attendance records to find consecutive absences
                for record in attendance_records:
                    if record['name_id'] == current_name_id:
                        if record['dates'] == previous_date + timedelta(days=1):
                            consecutive_absences_count += 1
                        else:
                            if consecutive_absences_count >= 7:
                                # Check if ContinuousAbsence record already exists for this name_id
                                existing_record = ContinuousAbsence.objects.filter(name_id=current_name_id).first()
                                if existing_record:
                                    # If ContinuousAbsence record exists, update the streak
                                    existing_record.streak += consecutive_absences_count
                                    existing_record.save()
                                else:
                                    # If ContinuousAbsence record doesn't exist, create a new one
                                    ContinuousAbsence.objects.create(
                                        name_id=current_name_id,
                                        streak=consecutive_absences_count,
                                        month=month,
                                        year=year
                                    )
                            consecutive_absences_count = 1
                    else:
                        if consecutive_absences_count >= 7:
                            existing_record = ContinuousAbsence.objects.filter(name_id=current_name_id).first()
                            if existing_record:
                                existing_record.streak += consecutive_absences_count
                                existing_record.save()
                            else:
                                ContinuousAbsence.objects.create(
                                    name_id=current_name_id,
                                    streak=consecutive_absences_count,
                                    month=month,
                                    year=year
                                )
                        consecutive_absences_count = 1

                    current_name_id = record['name_id']
                    previous_date = record['dates']

                # Handle the last student
                if consecutive_absences_count >= 7:
                    existing_record = ContinuousAbsence.objects.filter(name_id=current_name_id).first()
                    if existing_record:
                        existing_record.streak += consecutive_absences_count
                        existing_record.save()
                    else:
                        ContinuousAbsence.objects.create(
                            name_id=current_name_id,
                            streak=consecutive_absences_count,
                            month=month,
                            year=year
                        )

                objects_of_absencies = ContinuousAbsence.objects.filter(month=month,year=year)
                
                reduction_days = 0

                for i in objects_of_absencies:
                    reduction_days += i.streak
                    print(i.name,i.streak)
                
                print(reduction_days)

                total_mess_days = (number_of_students * mess_days) - reduction_days     #number of mess days after reducing reduction days

                print(f"Start date: {start_date}")
                print(f"End date: {end_date}")
                print(f"No of: Students {number_of_students}")
                print(f"total_mess_amount: {total_mess_amount}")
                print(f"room_rent: {room_rent}")
                print(f"staff_salary: {staff_salary}")
                print(f"electricity_bill: {electricity_bill}")
                print(f"total reduction days: {reduction_days}")
                print(f"mess_days: {mess_days}")
                print(f"Total mess days: {total_mess_days}")

                mess_bill_per_day = total_mess_amount / total_mess_days     #per day charge for mess
                other_expenses_per_student = ((room_rent*number_of_students) + (staff_salary + electricity_bill)) / number_of_students     #other expences
                
                print(f"mess_bill_per_day: {mess_bill_per_day}")
                print(f"other_expenses_per_student: {other_expenses_per_student}")

                students = Student.objects.all()
                
                absent_student_ids = objects_of_absencies.values_list('name_id', flat=True)
                students_with_absences = students.filter(id__in=absent_student_ids)
                
                sum = 0

                for student in students:
                    if student in students_with_absences:
                        name_id = student.id
                        obj = ContinuousAbsence.objects.filter(name_id=name_id)
                        streak = obj.get().streak
                        days_present = mess_days - streak
                        print(f"{name_id} absent for {streak} days & present for {days_present} days")
                        mess_bill = round((mess_bill_per_day * days_present) + other_expenses_per_student, 2)
                        sum += mess_bill
                        print(f"Mess bill: {mess_bill}")
                        student_bill = StudentBill(name=student, total=mess_bill, month=month, year=year) 
                        student_bill.save() 
                    else:
                        name_id = student.id
                        days_present = mess_days
                        print(f"{name_id} present for {days_present} days")
                        mess_bill = round((mess_bill_per_day * days_present) + other_expenses_per_student, 2)
                        sum += mess_bill
                        print(f"Mess bill: {mess_bill}")
                        student_bill = StudentBill(name=student, total=mess_bill, month=month, year=year) 
                        student_bill.save() 

                print(f"sum: {sum}")

                return redirect('view_monthly_bill',month,year)
    else:
        form = BillForm()
    return render(request, "hostel/billform.html", {'form': form})

@login_required()
def view_bill(request):
    context = StudentBill.objects.all().select_related('name')
    return render(request,"hostel/bill.html",{'bills':context})

@login_required()
def view_monthly_bill(request,month,year):
    current_month = month
    current_year = year
    bills = StudentBill.objects.filter(month=current_month,year=current_year).select_related('name')
    return render(request,"hostel/month_bill.html",{'bills':bills})

