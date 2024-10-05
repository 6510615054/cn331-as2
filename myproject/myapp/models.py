from django.db import models

# Create your models here.

class Student(models.Model):
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    sID = models.CharField(max_length=10)
    idCard = models.CharField(max_length=13)
    date = models.DateField(auto_now_add=True)
    faculty = models.CharField(max_length=100)
    department = models.CharField(max_length=100)

    # แสดงผลในตาราง person เป็นชื่อ ในหน้าของ admin
    def __str__(self):
        return str(self.sID) + " " + self.fname
    
class Subject(models.Model):
    sjID = models.CharField(max_length=10)
    sName = models.CharField(max_length=100)
    eduSec = models.CharField(max_length=1)
    eduYear = models.IntegerField()
    seatAva = models.IntegerField()
    status = models.BooleanField()

    def __str__(self):
        return str(self.sjID) + " " + self.sName

class Regis(models.Model):
    Student.sID
    Subject.sjID
    