from django.urls import path,include
from .views import RegistrationView,LoginView,ChangePasswordView,CourseView,CourseModiView,CourseAssignAdminView,CourseAdminView
from rest_framework.routers import DefaultRouter


route = DefaultRouter()

route.register(r'courseassign',CourseAssignAdminView,basename="courseassign_detail")
route.register(r'course',CourseAdminView,basename="course_detail")


urlpatterns = [
    path('register/',RegistrationView.as_view(),name='register'),
    path('login/',LoginView.as_view(),name='login'),
    path('changepwd/',ChangePasswordView.as_view(),name='changepwd'),
    path('course/',CourseView.as_view(),name='courses'),
    path('course/<int:pk>/',CourseModiView.as_view(),name='course_detail'),
    # admin  urls ...
    path('admin/',include(route.urls)),
    
]
