from django.urls import path
from myapp import views

urlpatterns = [
    path('', views.login, name='login'),
    path('register', views.register, name='register'),
    path('homepage', views.homepage, name='homepage'),
    path('logout', views.logout, name='logout'),
    path('userInfo', views.userInfo, name='user_info'),
    path('viewCourse', views.viewCourse, name='view_course'),
    path('enroll', views.enroll, name='enroll'),  # Updated for clarity in tests
    path('result', views.result, name='result'),
    path('withdraw', views.withdraw, name='withdraw'),  # Original withdraw URL
    path('add/<student_id>/<subject_id>', views.add, name='add_subject'),
    path('myCourse', views.myCourse, name='my_course'),
    path('delete/<student_id>/<subject_id>', views.delete, name='delete_subject'),
    path('enrollSubmit/<student_id>', views.enrollSubmit, name='enroll_submit'),
    path('withdrawal/<student_id>/<subject_id>', views.withdrawal, name='withdraw_subject'),  # Renamed for withdraw test
    path('change_password/', views.change_password, name='change_password'),
    path('admindecide', views.admindecide, name='admin_decide'),
    path('adminview/', views.admin_view, name='admin_view')
]
