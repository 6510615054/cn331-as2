from django.shortcuts import render,redirect
from myapp.models import Student,Subject,Register,TempRegister
from django.contrib import messages

# Create your views here.
def login(request):

    if request.method == 'POST':
        # รับข้อมูล
        sID = request.POST["sID"]
        idCard = request.POST["idCard"]

        if((sID == 'admin') and (idCard == 'admin')):
            return redirect('/admin')
        
        try:
            student = Student.objects.get(sID=sID, idCard=idCard)

            # เก็บค่า sID เพื่อไปแสดงผลหน้าอื่นด้วย
            request.session['student_id'] = student.sID

            return render(request, 'index.html',{'Student':student})

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
    subjects = Subject.objects.all()
    return render(request,'result.html',{'Student':student, "Subject":subjects})

def withdraw(request):
    student = Student.objects.get(sID=request.session.get('student_id'))
    subjects = Subject.objects.all()
    return render(request,'withdraw.html',{'Student':student, "Subject":subjects})

def add(request, student_id, subject_id):
    if request.method == 'GET':
        
        student = Student.objects.get(sID=student_id)
        subject = Subject.objects.get(sjID=subject_id)

        temp_newRegis = TempRegister.objects.create(
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

            new_regis.save()

        regis.delete()
        messages.success(request,'ลงทะเบียนสำเร็จ')
        return redirect('/homepage')

    return redirect('/myCourse')