from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.messages import get_messages
from .models import Student, Subject, Register, TempRegister
import json

class LoginViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.student = Student.objects.create(
            fname="Alice",
            lname="Johnson",
            sID="654321",
            idCard="B1234567890123",
            faculty="Arts",
            department="History"
        )

        self.admin = Student.objects.create(
            fname="admin",
            lname="admin",
            sID="admin",
            idCard="admin",
            faculty="admin",
            department="admin"
        )

    def test_login_success_client(self):
        response = self.client.post(reverse("login"), {
            "sID": self.student.sID,
            "idCard": self.student.idCard
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")

    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    def test_login_failure_client(self):
        response = self.client.post(reverse("login"), {
            "sID": self.student.sID,
            "idCard": "wrong_password"
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login.html")

        # Get the messages from the response
        messages = list(get_messages(response.wsgi_request))

        # Check that the expected error message is in the messages
        self.assertTrue(any(msg.message == "รหัสนักศึกษาหรือบัตรประชาชนไม่ถูกต้อง!" for msg in messages))

    def test_login_success_admin(self):
        response = self.client.post(reverse("login"), {
            "sID": "admin",
            "idCard": "admin"
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/admindecide")

        response_admin_views = self.client.post(reverse("admin_view"))
        self.assertEqual(response_admin_views.status_code, 200)
        self.assertTemplateUsed(response_admin_views, "adminview.html")

class RegisterViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_register_success_view_post(self):
        response = self.client.post(reverse("register"), {
            "fname": "Michael",
            "lname": "Scott",
            "sID": "987654",
            "idCard": "C1234567890123",
            "faculty": "Business",
            "department": "Management"
        })
        self.assertEqual(response.status_code, 302)  # Redirect after registration
        self.assertRedirects(response, "/")
        self.assertTrue(Student.objects.filter(sID="987654").exists())
    
    def test_register_failure_view_post(self):
        response = self.client.post(reverse("register"), {
            "fname": "Michael",
            "lname": "Scott",
            "sID": "",
            "idCard": "",
            "faculty": "",
            "department": "Management"
        })
        self.assertEqual(response.status_code, 302) 
        self.assertRedirects(response, "/register")


class PageViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.student = Student.objects.create(
            fname="Alice",
            lname="Johnson",
            sID="654321",
            idCard="B1234567890123",
            faculty="Arts",
            department="History"
        )
        self.client.post(reverse("login"), {"sID": "654321", "idCard": "B1234567890123"})

    def test_register_view_get(self):
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "register.html")

    def test_homepage_view_get(self):
        response = self.client.get(reverse("homepage"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")

    def test_enroll_view(self):
        response = self.client.get(reverse("enroll"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "enroll.html")

    def test_myCourse_view(self):
        response = self.client.get(reverse("my_course"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "myCourse.html")

    def test_result_view(self):
        response = self.client.get(reverse("result"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "result.html")

    def test_userInfo_view(self):
        response = self.client.get(reverse("user_info"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "userInfo.html")

    def test_viewCourse_view(self):
        response = self.client.get(reverse("view_course"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "viewCourse.html")

    def test_withdraw_view(self):
        response = self.client.get(reverse("withdraw"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "withdraw.html")
    
    def test_logout_view_get(self):
        response = self.client.get(reverse("logout"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/")


class EnrollSubjectTest(TestCase):
    def setUp(self):
        # Create a student
        self.client = Client()
        self.student = Student.objects.create(
            fname="John",
            lname="Doe",
            sID="123456",
            idCard="A1234567890123",
            faculty="Science",
            department="Physics"
        )

        # Create a subject with available seats
        self.subject = Subject.objects.create(
            sjID="PHY101",
            sName="Physics",
            eduSec="A",
            eduYear=1,
            maxSeat=30,
            seatAva=10,  # Initial available seats
            status=True
        )
        
        self.client.post(reverse("login"), {"sID": "123456", "idCard": "A1234567890123"})

    def test_add_subjects(self):

        # test add subjects
        response_add = self.client.get(reverse("add_subject", args=[self.student.sID,self.subject.sjID]))
        
        self.assertTrue(TempRegister.objects.filter(sID=self.student.sID,sjID=self.subject.sjID).exists())
        self.assertEqual(response_add.status_code, 302)
        self.assertRedirects(response_add, "/enroll")

    def test_enroll_subjects(self):

        EnrollSubjectTest.test_add_subjects(self)
        initial_seatAva = self.subject.seatAva
        # test enroll subjects
        response_enroll_1 = self.client.post(reverse("enroll_submit", args=[self.student.sID]))
        self.assertEqual(response_enroll_1.status_code, 302)  
        self.assertRedirects(response_enroll_1,'/myCourse')

        response_enroll_2 = self.client.get(reverse("enroll_submit", args=[self.student.sID]))

        self.subject.refresh_from_db()

        self.assertTrue(Register.objects.filter(sID=self.student.sID, sjID=self.subject.sjID).exists())
        self.assertEqual(self.subject.seatAva, initial_seatAva - 1)
        self.assertEqual(response_enroll_2.status_code, 302)  
        self.assertRedirects(response_enroll_2,'/homepage')

    def test_withdraw_subjects(self):
        
        EnrollSubjectTest.test_add_subjects(self)
        EnrollSubjectTest.test_enroll_subjects(self)
        # test withdraw subjects
        after_enroll_seatAva = self.subject.seatAva

        response_withdraw = self.client.get(reverse("withdraw_subject", args=[self.student.sID,self.subject.sjID]))

        self.subject.refresh_from_db()

        self.assertFalse(Register.objects.filter(sID=self.student.sID, sjID=self.subject.sjID).exists())
        self.assertEqual(self.subject.seatAva, after_enroll_seatAva + 1)
        self.assertEqual(response_withdraw.status_code, 302)  
        self.assertRedirects(response_withdraw,'/homepage')

    def test_login_again(self):
        # test for field isPicked is updated
        EnrollSubjectTest.test_add_subjects(self)
        EnrollSubjectTest.test_enroll_subjects(self)

        self.client.get(reverse("logout"))
        self.client.post(reverse("login"), {"sID": self.student.sID, "idCard": self.student.idCard})
        self.assertTrue(Register.objects.filter(sID=self.student.sID, sjID=self.subject.sjID).exists())
        registers = Register.objects.filter(sID=self.student.sID, sjID=self.subject.sjID)
        for reg in registers: 
            subject = Subject.objects.get(sjID=reg.sjID) 
            self.assertTrue(subject.isPicked == True)


class ChangePasswordTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.student = Student.objects.create(
            fname="Alice",
            lname="Johnson",
            sID="654321",
            idCard="B1234567890123",
            faculty="Arts",
            department="History"
        )

    def test_change_password(self):
        response = self.client.post(reverse("change_password"), data=json.dumps({
            "id": "654321",
            "new_password": "new_password123"
        }), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.student.refresh_from_db()
        self.assertEqual(self.student.idCard, "new_password123")

