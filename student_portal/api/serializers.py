from rest_framework import serializers
from .models import User,Course,Course_assign,Attendance,Assignment,Assign_Submit
from django.contrib.auth.hashers import make_password


PAYMENT_MOOD = [
        ('online','ONLINE MOOD'),
        ('offline','OFFLINE MOOD')
    ]

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,min_length=6,style={"input_type":"password"})
    confirm_password = serializers.CharField(write_only=True,min_length=6,style={"input_type":"password"})

    class Meta:
        model = User
        fields = ['email','username','password','confirm_password']

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.pop('confirm_password')
        if password != password2:
            raise serializers.ValidationError("Password and Conform Password doesn't match .")
        attrs['password'] = make_password(password)
        return attrs
    



class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(style={'input_type':'password'})



class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255,style={'input_type':'password'},write_only=True)
    password_conform = serializers.CharField(max_length=255,style={'input_type':'password'},write_only=True)
    class Meta:
        fields = ['password','password_conform']

    def validate(self, attrs):
        password = attrs.get('password')
        password_conform = attrs.get('password_conform')
        user = self.context.get('user')
        if password !=password_conform:
            raise serializers.ValidationError("Password and Conform Password doesn't match.")
        user.set_password(password)
        user.save()
        return attrs


class CourseSerializer(serializers.ModelSerializer):
    faculty = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Course
        fields = ['course_name','slug','description','fees','duration','faculty']

class CourseAssignSerializer(serializers.ModelSerializer):

    student = serializers.StringRelatedField(read_only=True,many=True)
    course = serializers.StringRelatedField(read_only=True,many=True)
    payment_mood = serializers.ChoiceField(choices=PAYMENT_MOOD)
    class Meta:
        model = Course_assign
        fields = ['student','course','payment_mood','paid_fees','due_fees','admission','expire_at']



# attendance serialier classes...
class AttendanceSerializer(serializers.ModelSerializer):
    course = serializers.StringRelatedField(read_only=True,many=True)
    class Meta:
        model = Attendance
        fields = ['course','attendance']


class AssignmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Assignment
        fields = ['assign_course','title','assignment','created_at','updated_at']


class AssignmentSubmitSerialier(serializers.ModelSerializer):
    student = serializers.StringRelatedField(read_only=True,many=True)
    course = serializers.StringRelatedField(read_only=True,many=True)
    class Meta:
        model = Assign_Submit
        fields = ['student','course','assign_file','total_mark','obtain_mark','grade','feedback','submited_at']
