from django.urls import path,include
from .views import RegistrationView,LoginView,ChangePasswordView,CourseView,CourseAssignView,StudentCourseView,AttendanceView,AssignmentView,AssignmentCheckView,MySubmitAssignView,StudentAttendanceView,ProfileView,AdminUserView
from rest_framework.routers import DefaultRouter


route = DefaultRouter()

route.register('course',CourseView,basename='course_detail')
route.register('course/assign',CourseAssignView,basename='courseassign_detail')
route.register('attendance',AttendanceView,basename='attendance_detail')
route.register('assignment',AssignmentView,basename='assignment_detail')
route.register('assignment/checked',AssignmentCheckView,basename='assignment_checked_detail')
route.register('admin/control/user/',AdminUserView,basename='admin_access')

urlpatterns = [
    path('register/',RegistrationView.as_view(),name='register'),
    path('login/',LoginView.as_view(),name='login'),
    path('profile/',ProfileView.as_view(),name='profile'),
    path('changepwd/',ChangePasswordView.as_view(),name='changepwd'),
    path('mycourse/assign',StudentCourseView.as_view(),name='mycourses'),
    path('mycourse/assign/<int:pk>/',StudentCourseView.as_view()),
    path('mycourse/assign/<int:pk>/',StudentCourseView.as_view()),
    path('myattendance/',StudentAttendanceView.as_view()),
    path('myattendance/<int:pk>/',StudentAttendanceView.as_view()),
    path('myassign/submit/',MySubmitAssignView.as_view()),
    path('myassign/submit/<int:pk>/',MySubmitAssignView.as_view()),
    path('',include(route.urls)),
    
    
    
]
