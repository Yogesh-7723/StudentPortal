from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.core.validators import MinValueValidator,MaxValueValidator
from django.core.validators import RegexValidator
from django.utils.text import slugify
from datetime import timedelta,datetime



class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None,**extra_fields):
        
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            **extra_fields
            
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None,**extra_fields):
        extra_fields.setdefault('is_active',True)
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_admin',True)
        extra_fields.setdefault('is_student',False)
        
        user = self.create_user(
            email,
            password=password,
            username=username,
            **extra_fields
        )
        
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('completed','COMPLETED'),
        ('drop','DROP'),
        ('active','ACTIVE'),
    ]

    USER_ROLES = [
        ('student','STUDENT'),
        ('faculty','FACULTY'),
    ]

    email = models.EmailField(
        verbose_name="Email",
        max_length=255,
        unique=True,
    )
    username = models.CharField(max_length=200)
    first_name = models.CharField(max_length=200,blank=True,null=True)
    last_name = models.CharField(max_length=200,blank=True,null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES,blank=True,null=True)
    contact = models.CharField(
    max_length=10,
    unique=True,
    validators=[RegexValidator(regex=r'^\d{10}$', message="Enter a valid 10-digit contact number.")],blank=True,null=True
    )
    date_of_birth = models.DateField(blank=True,null=True)
    # role = models.CharField(choices=USER_ROLES,max_length=10,blank=True,null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES,blank=True,null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_student = models.BooleanField(default=True)
    is_faculty = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.username

    def has_perm(self,perm,obj=None):
        return self.is_superuser
    
    def has_module_perms(self,app_label):
        return self.is_superuser
    

# course tables...

class Course(models.Model):
    course_name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True)
    description = models.TextField()
    fees = models.DecimalField(max_digits=10,decimal_places=2)
    duration = models.PositiveIntegerField(help_text="course duration write in days |")
    faculty = models.ForeignKey(User,on_delete=models.RESTRICT,limit_choices_to={'is_faculty':True})

    def save(self,*args,**kwargs):
        self.slug = slugify(self.course_name)
        super(Course,self).save(*args,**kwargs)


class Course_assign(models.Model):
    PAYMENT_MOOD = [
        ('online','ONLINE MOOD'),
        ('offline','OFFLINE MOOD')
    ]

    student = models.ForeignKey(User,on_delete=models.PROTECT,limit_choices_to={'is_student':True})
    course = models.ForeignKey(Course,on_delete=models.PROTECT)
    payment_mood = models.CharField(choices=PAYMENT_MOOD,max_length=10)
    paid_fees = models.DecimalField(max_digits=10,decimal_places=2)
    due_fees = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    admission = models.DateTimeField(auto_now_add=True)
    expire_at = models.DateTimeField(blank=True,null=True)

    def save(self, *args, **kwargs):
        self.expire_at = self.admission + timedelta(days=self.course.duration)
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.course.course_name} assign to {self.student.username}"
    

class Attendance(models.Model):
    course = models.OneToOneField(Course_assign, on_delete=models.CASCADE, related_name="course_attendance")
    attendance = models.PositiveBigIntegerField(default=0)
    atten_date = models.DateField(auto_now=True)


class Assignment(models.Model):
    assign_course = models.ForeignKey(Course,on_delete=models.CASCADE,related_name="course_assignment")
    title = models.CharField(max_length=200)
    assignment = models.TextField()
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

class Assign_Submit(models.Model):
    student = models.ForeignKey(User,on_delete=models.CASCADE,related_name="student_submit_assign",limit_choices_to={'is_student':True})
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    assign_file = models.FileField(upload_to='assignments')
    total_mark = models.PositiveBigIntegerField(default=100,blank=True,null=True)
    obtain_mark = models.PositiveBigIntegerField(default=100,blank=True,null=True)
    grade = models.CharField(max_length=5,blank=True,null=True)
    feedback = models.TextField()
    submited_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)
    check_by = models.CharField(max_length=250,blank=True,null=True)
     

    
    
    


    

    