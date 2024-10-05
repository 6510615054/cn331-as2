from django.shortcuts import render,redirect,get_object_or_404
from myapp.models import Student,Subject,Regis,Register,TempRegister
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from django.db.models import Q 
import json

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib import messages
from myapp.models import Student

def login(request):
    if request.method == 'POST':
        # รับข้อมูล
        sID = request.POST["sID"]
        idCard = request.POST["idCard"]

        if((sID == 'admin') and (idCard == 'admin')):
            return redirect('/admin')
        
        try:
            student = Student.objects.get(sID=sID, idCard=idCard)

            # Check if the idCard matches the stored password
            if student.idCard == idCard:  # Direct comparison
                # เก็บค่า sID เพื่อไปแสดงผลหน้าอื่นด้วย
                request.session['student_id'] = student.sID
                return render(request, 'index.html', {'Student': student})
            else:
                messages.error(request, "รหัสนักศึกษาหรือบัตรประชาชนไม่ถูกต้อง!")  # Incorrect password

        except Student.DoesNotExist:
            # ถ้าไม่พบผู้ใช้ ให้แสดงข้อความผิดพลาด
            messages.error(request, "รหัสนักศึกษาหรือบัตรประชาชนไม่ถูกต้อง!")

    return render(request, 'login.html')


def register(request):
     
    if request.method == 'POST':
        # รับข้อมูล
        fname = request.POST["fname"]
        lname = request.POST["lname"]
        sID = request.POST["sID"]
        idCard = request.POST["idCard"]
        faculty = request.POST["faculty"]
        department = request.POST["department"]
        
        if not fname or not lname or not sID or not idCard:
            messages.error(request, "กรุณากรอกข้อมูลให้ครบถ้วน!")
            return redirect('/register')

        # บันทึกข้อมูล
        new_student = Student.objects.create(
            fname = fname,
            lname = lname,
            sID = sID,
            idCard = idCard,
            faculty = faculty,
            department = department
        )

        new_student.save()
        messages.success(request,"ลงทะเบียนสำเร็จ")
        # เปลี่ยนเส้นทางไปหน้าแรก
        return redirect('/')
    else:
        return render(request,'register.html')
    
def homepage(request):

    # ดึงข้อมูล student จาก sID ที่บันทึกมาจาก login
    student = Student.objects.get(sID=request.session.get('student_id'))
    return render(request,'index.html',{'Student':student})

def logout(request):

    if 'student_id' in request.session:
        del request.session['student_id']

    return redirect('/')

def userInfo(request):
    student = Student.objects.get(sID=request.session.get('student_id'))
    return render(request,'userInfo.html',{'Student':student})

def viewCourse(request):
    student = Student.objects.get(sID=request.session.get('student_id'))
    subjects = Subject.objects.all()
    return render(request,'viewCourse.html',{'Student':student, "Subject":subjects})

def enroll(request):
    student = Student.objects.get(sID=request.session.get('student_id'))
    subjects = Subject.objects.all()
    return render(request,'enroll.html',{'Student':student, "Subject":subjects})

def result(request):
    student = Student.objects.get(sID=request.session.get('student_id'))
    data = Register.objects.filter(sID=student.sID)
    return render(request,'result.html',{'data':data,'Student':student})

def withdraw(request):
    student = Student.objects.get(sID=request.session.get('student_id'))
    data = Register.objects.filter(sID=student.sID)
    return render(request,'withdraw.html',{'data':data,'Student':student})

def add(request, student_id, subject_id):
    if request.method == 'GET':
        
        student = Student.objects.get(sID=student_id)
        subject = Subject.objects.get(sjID=subject_id)

        temp_newRegis = TempRegister.objects.create(
            student=student,
            subject=subject,
            fname = student.fname,
            lname = student.lname,
            sID = student.sID,
            sjID = subject.sjID,
            sName = subject.sName
        )

        subject.isPicked = True
        subject.save()
        temp_newRegis.save()

    return redirect('/enroll')


def myCourse(request):
    student = Student.objects.get(sID=request.session.get('student_id'))
    subjects = TempRegister.objects.filter(sID=request.session.get('student_id'))
    return render(request,'myCourse.html',{'Student':student,"subjects":subjects})

def change_password(request):
    if request.method == 'POST':
        # Ensure the request body is JSON
        try:
            data = json.loads(request.body)
            student_id = data.get('id')
            new_password = data.get('new_password')

            # Get the student object using the student ID
            student = Student.objects.get(sID=student_id)
            
            # Set the new password
            student.idCard = new_password  # Assuming you want to store the new password in idCard
            student.save()  # Save the changes to the database
            
            return JsonResponse({'success': True})
        except Student.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Student not found'})
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

def admindecide(request):
    return render(request,'admindecide.html')

def admin_view(request):
    query = request.GET.get('query', '')
    students = Student.objects.all()

    if query:
        # Filtering students based on the search query
        students = students.filter(
            Q(sID__icontains=query) |  # Search by Student ID
            Q(fname__icontains=query) |  # Search by First Name
            Q(lname__icontains=query)    # Search by Last Name
        ).distinct()

    context = {
        'students': students,
    }
    return render(request, 'adminview.html', context)

def delete(request, student_id, subject_id):
    if request.method == 'GET':

        temp_regis = TempRegister.objects.get(sjID=subject_id,sID= student_id)
        subject = Subject.objects.get(sjID=subject_id)

        subject.isPicked = False
        subject.save()

        temp_regis.delete()

    return redirect('/myCourse')


def enrollSubmit(request, student_id):
    if request.method == 'GET':

        regis = TempRegister.objects.filter(sID= student_id)

        for item in regis:
            new_regis = Register.objects.create(
                fname=item.fname,
                lname=item.lname,
                sID=item.sID,
                sjID=item.sjID,
                sName=item.sName
            )

            subject = Subject.objects.get(sjID=item.sjID)

            if subject.seatAva > 0:
                subject.seatAva -= 1
            
            subject.save()
            new_regis.save()

        regis.delete()
        messages.success(request,'ลงทะเบียนสำเร็จ')
        return redirect('/homepage')

    return redirect('/myCourse')


def withdrawal(request, student_id, subject_id):
    if request.method == 'GET':

        regis = Register.objects.get(sjID=subject_id,sID= student_id)
        subject = Subject.objects.get(sjID=subject_id)

        subject.isPicked = False
        subject.seatAva += 1
        subject.save()

        regis.delete()
        messages.success(request,'ถอนรายวิชาสำเร็จ')

    return redirect('/homepage')