from django.contrib import admin
from .models import Customuser,PersonalInfo,AdditionalInfo, UserMedia,Employee,Jobseeker,FriendRequest
# Register your models here.
admin.site.register(Customuser)
admin.site.register(PersonalInfo)
admin.site.register(AdditionalInfo)
admin.site.register(UserMedia)
admin.site.register(Employee)
admin.site.register(Jobseeker)
admin.site.register(FriendRequest)
