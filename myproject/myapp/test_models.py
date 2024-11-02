from django.test import TestCase, Client
from .models import Student, Subject, Register, TempRegister
import json

class StudentModelTest(TestCase):
    def setUp(self):
        self.student = Student.objects.create(
            fname="John",
            lname="Doe",
            sID="1234567890",
            idCard="1234567890123",
            faculty="Engineering",
            department="Computer"
        )

    # test correct data
    def test_student_creation(self):
        self.assertEqual(self.student.fname, "John")
        self.assertEqual(self.student.lname, "Doe")
        self.assertEqual(self.student.sID, "1234567890")
        self.assertEqual(str(self.student), "1234567890 John")

class SubjectModelTest(TestCase):
    def setUp(self):
        self.subject_with_seatava = Subject.objects.create(
            sjID="PHY101",
            sName="Physics",
            eduSec=1,
            eduYear=2567,
            maxSeat=30,
            seatAva=30,
            status=True
        )

        self.subject_without_seatava = Subject.objects.create(
            sjID="CAL101",
            sName="Calculus",
            eduSec=1,
            eduYear=2567,
            maxSeat=20,
            seatAva=0,
            status=False
        )

    # test correct data
    def test_subject_creation(self):
        self.assertEqual(self.subject_with_seatava.sjID, "PHY101")
        self.assertEqual(self.subject_with_seatava.sName, "Physics")
        self.assertEqual(str(self.subject_with_seatava), "PHY101 Physics")

    # test subject's status
    def test_subject_status_with_seats(self):
        self.subject_with_seatava.refresh_from_db()
        self.assertTrue(self.subject_with_seatava.status)

    # test subject's status
    def test_subject_status_no_seats(self):
        self.subject_without_seatava.refresh_from_db()
        self.assertFalse(self.subject_without_seatava.status)

    # test update status
    def test_subject_status_updates(self):
        self.subject_with_seatava.seatAva = 0
        self.subject_with_seatava.save()
        self.assertFalse(self.subject_with_seatava.status) 


class RegisterModelTest(TestCase):
    def setUp(self):
        self.register = Register.objects.create(
            fname="Jane",
            lname="Smith",
            sID="123457",
            sjID="MAT101",
            sName="Mathematics"
        )

    # test correct data
    def test_register_creation(self):
        self.assertEqual(str(self.register), "MAT101 123457")
