from django.urls import path
from myapp import views

urlpatterns = [
    path('',views.login),
    path('register',views.register),
    path('homepage',views.homepage),
    path('logout',views.logout),
    path('userInfo',views.userInfo),
    path('viewCourse',views.viewCourse),
    path('enroll',views.enroll),
    path('result',views.result),
    path('withdraw',views.withdraw),
    path('add/<student_id>/<subject_id>', views.add),
    path('myCourse',views.myCourse),
    path('delete/<student_id>/<subject_id>', views.delete),
    path('enrollSubmit/<student_id>', views.enrollSubmit),
    path('withdrawal/<student_id>/<subject_id>', views.withdrawal),
]
