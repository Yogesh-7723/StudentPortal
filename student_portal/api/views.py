from django.shortcuts import render
from .models import User,Course,Course_assign,Attendance,Assignment,Assign_Submit
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RegisterSerializer,LoginSerializer,ChangePasswordSerializer,CourseSerializer,CourseAssignSerializer,AttendanceSerializer,AssignmentCheckSerializer,AssignmentSerializer,MySubmitAssignSerializer,UserSerializer
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .errorenderer import UserRenderer
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView,ListAPIView
from rest_framework.decorators import api_view
from .custompermission import StudentReadOnlyPerm,AdminFacultyPerm,IsStudentPerm

# Create your views here.


def get_user_token(user):
    refresh = RefreshToken.for_user(user)
    response = {
        "refresh": str(refresh),
        "access": str(refresh.access_token)
    }
    return response




class RegistrationView(APIView):
    def post(self,request,format=True):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success":"Registration Successfully !"},status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
        
class LoginView(APIView):
    renderer_classes = [UserRenderer]
    def post(self,request,format=None):
        serialize = LoginSerializer(data=request.data)
        if serialize.is_valid(raise_exception=True):
            email = serialize.validated_data.get('email')
            password = serialize.validated_data.get('password')
            user = authenticate(email=email,password=password)
            if user is not None:
                token = get_user_token(user)
                return Response({'msz':"Login success","token":token},status=status.HTTP_200_OK)
            else:
                return Response({'errors':{"non_field_errors":['Email or Password is not Valid']}},status=status.HTTP_400_BAD_REQUEST)
        return Response(serialize.errors,status=status.HTTP_400_BAD_REQUEST)



class ChangePasswordView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self,request,format=None):
        serializer = ChangePasswordSerializer(data=request.data,context={'user':request.user})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Password Changed Successfully'},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

class ProfileView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request,format=None):
        email = request.user.email
        profile = User.objects.get(email=email)
        serializer = UserSerializer(profile)
        return Response(serializer.data,content_type='application/json',status=status.HTTP_200_OK)
    
    def patch(self,request,format=None):
        email = request.user.email
        profile = User.objects.get(email=email)
        serializer = UserSerializer(profile,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,content_type='application/json',status=status.HTTP_206_PARTIAL_CONTENT)
        else:
            return Response(serializer.errors,content_type='application/json',status=status.HTTP_400_BAD_REQUEST)

    

# permitted for admin and faculty only ...

class CourseView(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [StudentReadOnlyPerm]


class CourseAssignView(ModelViewSet):
    queryset = Course_assign.objects.all()
    serializer_class = CourseAssignSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [AdminFacultyPerm]


class AttendanceView(ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [AdminFacultyPerm]


class AssignmentView(ModelViewSet):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [StudentReadOnlyPerm]


class AssignmentCheckView(ModelViewSet):
    queryset = Assign_Submit.objects.all()
    serializer_class = AssignmentCheckSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [AdminFacultyPerm]


  



# only for student use...

class StudentCourseView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsStudentPerm]
    def get(self,request,format=None,pk=None):
        if pk is not None:
            course = Course_assign.objects.filter(student=request.user,pk=pk)
            serializer = CourseAssignSerializer(course)
            return Response(serializer.data,content_type="application/json",status=status.HTTP_201_CREATED)
        course = Course_assign.objects.filter(student=request.user)
        serializer = CourseAssignSerializer(course,many=True)
        return Response(serializer.data,content_type="application/json",status=status.HTTP_201_CREATED)
    
class StudentAttendanceView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsStudentPerm]

    def get(self, request, format=None):
        try:
            attendance = Attendance.objects.filter(course__student=request.user)
            
        except Attendance.DoesNotExist:
            return Response({"error": "Attendance record not found"}, status=status.HTTP_404_NOT_FOUND)
        
        else:
            serializer = AttendanceSerializer(attendance, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        


class MySubmitAssignView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsStudentPerm]
    def get(self,request,format=None,pk=None):
        if pk is not None:
            try:
                myassign = Assign_Submit.objects.get(student=request.user,pk=pk)
            except Exception as e:
                return Response({"warning":e},content_type='application/json',status=status.HTTP_404_NOT_FOUND)
            else:
                serializer = AssignmentCheckSerializer(myassign)
                return Response(serializer.data,content_type='application/json',status=status.HTTP_200_OK)
        myassign = Assign_Submit.objects.filter(student=request.user)
        serializer = MySubmitAssignSerializer(myassign,many=True)
        return Response(serializer.data,content_type='application/json',status=status.HTTP_200_OK)
    
    def post(self,request,format=None):
        serializer = MySubmitAssignSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data,content_type='application/json',status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,content_type='application/json',status=status.HTTP_400_BAD_REQUEST)
        

# admin profile control to any user...

class AdminUserView(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]