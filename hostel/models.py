from django.db import models

# Create your models here.

class Department(models.Model):
    dept_id = models.SmallIntegerField()
    dept_name = models.CharField(max_length=100)

    def __str__(self):
        return self.dept_name

class Programme(models.Model):
    pgm_id = models.SmallIntegerField()
    pgm_name = models.CharField(max_length=100)
    dept_id = models.ForeignKey(Department,on_delete=models.CASCADE)

    def __str__(self):
        return self.pgm_name

class Student(models.Model):
    name = models.CharField(max_length=50)
    category = models.CharField(max_length=20)
    pgm_id = models.ForeignKey(Programme,on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
class Room(models.Model):
    room_number = models.SmallIntegerField()
    floor = models.CharField(max_length=50)

    def __str__(self):
        return str(self.room_number)
    
class Allotment(models.Model):
    room_number = models.ForeignKey(Room,on_delete=models.CASCADE)
    name = models.ForeignKey(Student,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} in {self.room_number}"
    
class Attendance(models.Model):
    name = models.ForeignKey(Student,on_delete=models.CASCADE)
    dates = models.DateField()