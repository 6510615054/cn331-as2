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
    path('change_password/', views.change_password, name='change_password'),
    path('admindecide',views.admindecide),
    path('adminview/', views.admin_view, name='admin_view')
]
