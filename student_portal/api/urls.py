from django.urls import path,include
from .views import RegistrationView,LoginView,ChangePasswordView,CourseView,CourseAssignView,StudentCourseView
from rest_framework.routers import DefaultRouter


route = DefaultRouter()

route.register('course',CourseView,basename='course_detail')
route.register('course/assign',CourseAssignView,basename='courseassign_detail')


urlpatterns = [
    path('register/',RegistrationView.as_view(),name='register'),
    path('login/',LoginView.as_view(),name='login'),
    path('changepwd/',ChangePasswordView.as_view(),name='changepwd'),
    path('mycourse/',StudentCourseView.as_view(),name='mycourses'),
    path('mycourse/<int:pk>/',StudentCourseView.as_view()),
    path('',include(route.urls)),
    
    
    
]
