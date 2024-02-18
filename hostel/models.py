from django.db import models

# Create your models here.

class Department(models.Model):
    dept_id = models.SmallIntegerField(unique=True)
    dept_name = models.CharField(max_length=100,unique=True)

    def __str__(self):
        return self.dept_name

class Programme(models.Model):
    pgm_id = models.SmallIntegerField(unique=True)
    pgm_name = models.CharField(max_length=100,unique=True)
    dept_id = models.ForeignKey(Department,on_delete=models.CASCADE)

    def __str__(self):
        return self.pgm_name

class Student(models.Model):
    name = models.CharField(max_length=50, unique=True)

    obc = 'OBC'
    oec = 'OEC'
    gen = 'GENERAL'
    sc = 'SC'
    st = 'ST'

    category_choices = [(obc,'OBC'),(oec,'OEC'),(gen,"GENERAL"),(sc,'SC'),(st,'ST')]

    category = models.CharField(max_length=20,choices=category_choices)
    pgm_id = models.ForeignKey(Programme,on_delete=models.CASCADE)

    yes = 'YES'
    no = 'NO'

    egrantz_choice = [(yes,'Yes'),(no,'No')]  #Change is needed No to NO

    E_Grantz = models.CharField(max_length = 10,choices=egrantz_choice)

    def __str__(self):
        return self.name
    
class Room(models.Model):
    room_number = models.SmallIntegerField(unique=True)
    floor = models.CharField(max_length=50)

    def __str__(self):
        return str(self.room_number)
    
class Allotment(models.Model):
    room_number = models.ForeignKey(Room,on_delete=models.CASCADE)
    name = models.OneToOneField(Student,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} in {self.room_number}"
    
class Attendance(models.Model):
    name = models.ForeignKey(Student,on_delete=models.CASCADE)
    dates = models.DateField()

class MessBill(models.Model):
    no_of_students = models.SmallIntegerField()
    month = models.CharField(max_length=42)
    mess_days = models.SmallIntegerField()
    mess_amount = models.DecimalField(max_digits=10,decimal_places=2)
    room_rent = models.DecimalField(max_digits=10,decimal_places=2)
    staff_salary = models.DecimalField(max_digits=10,decimal_places=2)
    electricity_bill = models.DecimalField(max_digits=10,decimal_places=2)
    year = models.SmallIntegerField()

    def __str__(self):
        return self.month

class StudentBill(models.Model):
    name = models.ForeignKey(Student,on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10,decimal_places=2)
    month = models.CharField(max_length=20)
    year = models.SmallIntegerField()

    def __str__(self):
        return f"{self.name} - {self.month}"