from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User,Course,Course_assign,Attendance,Assignment,Assign_Submit

# Register your models here.


class UserAdmin(BaseUserAdmin):
    
    list_display = ('username','email','is_active','is_staff')
    list_filter = ('id','email','username')
    
    fieldsets = [
        (None, {"fields": ("email", "username", "password")}),
        ("Personal Information", {"fields": ("first_name", "last_name","contact","gender","date_of_birth")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser","is_admin","is_student","is_faculty",'last_login')}),
    ]

    add_fieldsets = [(None, {"fields": ("email", "password1",'password2')})]

    search_fields = ('email',)
    ordering = ('id',)
    filter_horizontal = ()

admin.site.register(User,UserAdmin)


#admin for course and course assign to students...

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id','course_name','description','fees','duration','faculty')
    list_filter = ('course_name','faculty')


@admin.register(Course_assign)
class CourseAssignAdmin(admin.ModelAdmin):
    list_display = ('id','student','payment_mood','paid_fees','due_fees','admission','expire_at')


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('course','attendance','atten_date')


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('assign_course','title','assignment','created_at','updated_at')


@admin.register(Assign_Submit)
class AssignmentSubmitAdmin(admin.ModelAdmin):
    list_display = ('student','course','assign_file','total_mark','obtain_mark','feedback','submited_at','check_by','status')
   