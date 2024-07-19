from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.conf import settings
import secrets
from datetime import date
# Create your models here.



class Customuser(AbstractUser):
    email = models.EmailField(unique=True)
    hidden_profiles = models.ManyToManyField('self', symmetrical=False, related_name='hidden_by')
    liked_profiles = models.ManyToManyField('self', symmetrical=False, related_name='liked_by', blank=True)
    liked_by_profiles = models.ManyToManyField('self', symmetrical=False, related_name='liked_profiles_reverse', blank=True)



    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )
    
    def __str__(self):
        return self.email

class OtpToken(models.Model):
    user = models.ForeignKey(Customuser, on_delete=models.CASCADE, related_name='otps')
    otp_code = models.CharField(max_length=6, default=secrets.token_hex(3))
    otp_created_at = models.DateTimeField(auto_now_add=True)
    otp_expires_at = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return self.user.username
    
class PersonalInfo(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    STATUS_CHOICES = [
        ('single', 'single'),
        ('in relationship', 'in relationship'),
        ('married', 'married'),
    ]
    user = models.OneToOneField(Customuser, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    fullname=models.CharField(max_length=25)
    DOB=models.DateField()
    gender=models.CharField(choices=GENDER_CHOICES,max_length=10)
    bio=models.TextField(blank=True)
    phone=models.CharField(max_length=12,null=True,blank=True)
    status=models.CharField(choices=STATUS_CHOICES,max_length=15)
    designation=models.CharField(max_length=25,null=True,blank=True)
    qualification=models.CharField(max_length=25)
    address=models.CharField(max_length=100)
    district=models.CharField(max_length=50,blank=True,null=True)
    state=models.CharField(max_length=50,blank=True,null=True)
    pincode=models.CharField(max_length=10)
    
    def __str__(self):
        return self.fullname
    
    def age(self):
        today = date.today()
        return today.year - self.DOB.year - ((today.month, today.day) < (self.DOB.month, self.DOB.day))
    
    
class AdditionalInfo(models.Model):
    INTREST_CHOICES=[
        ('male','male'),
        ('female','female'),
        ('both','both')
    ]
    DRINKING_CHOICES = [
        ('non_drinker', 'Non-Drinker'),
        ('social_drinker', 'Social Drinker'),
        ('regular_drinker', 'Regular Drinker'),
    ]

    SMOKING_CHOICES = [
        ('non_smoker', 'Non-Smoker'),
        ('occasional_smoker', 'Occasional Smoker'),
        ('regular_smoker', 'Regular Smoker'),
    ]
    user = models.OneToOneField(Customuser, on_delete=models.CASCADE)
    hobbies = models.CharField(max_length=255, help_text="Enter up to 5 hobbies separated by commas")
    intrested_in=models.CharField(choices=INTREST_CHOICES,max_length=50)
    drinking_habits = models.CharField(max_length=20, choices=DRINKING_CHOICES, default='non_drinker')
    smoking_habits = models.CharField(max_length=20, choices=SMOKING_CHOICES, default='non_smoker')
    weight = models.FloatField(null=True, blank=True)  
    height = models.FloatField(null=True, blank=True)
    
    def __str__(self):
        return self.user.username
    
    def get_hobbies_list(self):
        return self.hobbies.split(',')
    


class UserMedia(models.Model):
    user = models.OneToOneField(Customuser, on_delete=models.CASCADE)
    
    additional_image1 = models.ImageField(upload_to='additional_images/', blank=True, null=True)
    additional_image2 = models.ImageField(upload_to='additional_images/', blank=True, null=True)
    additional_image3 = models.ImageField(upload_to='additional_images/', blank=True, null=True)
    additional_image4 = models.ImageField(upload_to='additional_images/', blank=True, null=True)
    additional_image5 = models.ImageField(upload_to='additional_images/', blank=True, null=True)
    short_reel = models.FileField(upload_to='short_reels/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Media"
    def get_additional_images(self):
        images= [self.additional_image1, self.additional_image2, self.additional_image3, self.additional_image4, self.additional_image5] 
        return [image for image in images if image]
    
class Employee(models.Model):
    user = models.ForeignKey(Customuser, on_delete=models.CASCADE)
    position = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    company_name=models.CharField(max_length=100,blank=True,null=True)
    location = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.position}"

class Jobseeker(models.Model):
    EXPERTISE_CHOICES=[
        ('beginner','beginner'),
        ('intermediate','intermediate'),
        ('expert','expert')
    ]
    user = models.ForeignKey(Customuser, on_delete=models.CASCADE)
    title = models.CharField(max_length=100,null=True, blank=True)
    expertise_level = models.CharField(max_length=100,choices=EXPERTISE_CHOICES)

    def __str__(self):
        return f"{self.expertise_level}"
 
#friend request model

class FriendRequest(models.Model):
    id = models.AutoField(primary_key=True)
    from_user = models.ForeignKey(Customuser, related_name='friend_requests_sent', on_delete=models.CASCADE)
    to_user = models.ForeignKey(Customuser, related_name='friend_requests_received', on_delete=models.CASCADE)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.from_user} to {self.to_user}"