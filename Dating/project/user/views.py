from django.shortcuts import get_object_or_404, render,redirect
from django.urls import reverse_lazy
from django.views import View
from .forms import EmployeeForm, JobseekerForm, RegistrationForm, UserMediaForm
from .models import Customuser, FriendRequest, OtpToken,PersonalInfo,AdditionalInfo, UserMedia
from .forms import PersonalInfoForm,AdditionalInfoForm
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View, TemplateView, ListView, CreateView, UpdateView,DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.contrib.auth.decorators import login_required


def index(request):
    if request.user.is_authenticated:
        user_media = UserMedia.objects.filter(user=request.user).first()
        # Your other logic here
        return render(request, 'index.html', {'user_media': user_media})
    else:
        return render(request,'index.html')

class ContactView(View):
    def get(self, request):
        return render(request, 'contact.html')

class AboutView(View):
    def get(self, request):
        return render(request, 'about.html')

def signup(request):
    form = RegistrationForm()  # Instantiate the form
    
    if request.method == "POST":
        form = RegistrationForm(request.POST)  # Bind POST data to the form instance
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account created successfully! An OTP is sent to your email.')
            
            # Authenticate and log in the user
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            if user is not None:
                login(request, user)
                return redirect('create_pinfo')
            
            # If authentication fails, add an error message (optional)
            messages.error(request, 'Error logging in. Please try again.')
    
    # Context to be sent to the template
    context = {
        "form": form
    }
    
    return render(request, 'account/signup.html', context)

# def verify_email(request, username):
#     user = get_user_model().objects.get(username=username)
#     user_otp = OtpToken.objects.filter(user=user).last()
    
    
#     if request.method == 'POST':
#         # valid token
#         if user_otp.otp_code == request.POST['otp_code']:
            
#             # checking for expired token
#             if user_otp.otp_expires_at > timezone.now():
#                 user.is_active=True
#                 user.save()
#                 messages.success(request, "Account activated successfully!! You can Login.")
#                 return redirect("create_pinfo")
            
#             # expired token
#             else:
#                 messages.warning(request, "The OTP has expired, get a new OTP!")
#                 return redirect("verify-email", username=user.username)
        
        
#         # invalid otp code
#         else:
#             messages.warning(request, "Invalid OTP entered, enter a valid OTP!")
#             return redirect("verify-email", username=user.username)
        
#     context = {}
#     return render(request, "account/verify_token.html", context)

# def resend_otp(request):
#     if request.method == 'POST':
#         user_email = request.POST["otp_email"]
        
#         if get_user_model().objects.filter(email=user_email).exists():
#             user = get_user_model().objects.get(email=user_email)
#             otp = OtpToken.objects.create(user=user, otp_expires_at=timezone.now() + timezone.timedelta(minutes=5))
            
            
#             # email variables
#             subject="Email Verification"
#             message = f"""
#                                 Hi {user.username}, here is your OTP {otp.otp_code} 
#                                 it expires in 5 minute, use the url below to redirect back to the website
#                                 http://127.0.0.1:8000/verify-email/{user.username}
                                
#                                 """
#             sender = "clintonmatics@gmail.com"
#             receiver = [user.email, ]
        
        
#             # send email
#             send_mail(
#                     subject,
#                     message,
#                     sender,
#                     receiver,
#                     fail_silently=False,
#                 )
            
#             messages.success(request, "A new OTP has been sent to your email-address")
#             return redirect("verify-email", username=user.username)

#         else:
#             messages.warning(request, "This email dosen't exist in the database")
#             return redirect("resend-otp")
        
           
#     context = {}
#     return render(request, "account/resend_otp.html", context)


def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
         
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f"Hi {request.user.username}, you are now logged-in")
            return redirect("index")
        else:
            messages.warning(request, "Invalid credentials")
            return redirect("signin")
    
    return render(request, "account/login.html")



# class LoginView(View):
#     def get(self, request):
#         return render(request, 'account/login.html')



class MatchingView(View):
    def get(self, request):
        return render(request, 'matching_page.html')

class TestView(View):
    def get(self, request):
        return render(request, 'test.html')
class TestView2(View):
    def get(self, request):
        return render(request, 'test2.html')

class CreateProfileView(View):
    def get(self, request):
        return render(request, 'create_profile.html')

class ProfileView(LoginRequiredMixin, DetailView):
    model = PersonalInfo
    template_name = 'profile/profile.html'
    context_object_name = 'profile'

    def get_object(self):
        return get_object_or_404(PersonalInfo, user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['additional_info'] = get_object_or_404(AdditionalInfo, user=self.request.user)
        context['user_media'] = get_object_or_404(UserMedia, user=self.request.user)
        # Fetch the users who have liked the current user's profile
        context['liked_users']= self.request.user.liked_profiles.all()
        context['liked_by']=self.request.user.liked_by_profiles.all()
        return context

class PlansView(View):
    def get(self, request):
        return render(request, 'plans.html')
    

class P_info_CreateView(LoginRequiredMixin, CreateView):
    model = PersonalInfo
    form_class = PersonalInfoForm
    template_name = 'profile/create_pinfo.html'
    success_url = reverse_lazy('create_ainfo')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(P_info_CreateView,self).form_valid(form)
    
class P_info_UpdateView(LoginRequiredMixin,UpdateView):
    
    model = PersonalInfo
    form_class = PersonalInfoForm
    template_name = 'profile/create_pinfo.html'
    success_url = reverse_lazy('index')
    pk_url_kwarg = 'id'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
    
    


class A_info_CreateView(LoginRequiredMixin,CreateView):
    model=AdditionalInfo
    form_class=AdditionalInfoForm
    template_name='profile/create_ainfo.html'
    success_url=reverse_lazy('create_media')
    
    def form_valid(self, form):
        form.instance.user =self.request.user
        return super(A_info_CreateView,self).form_valid(form)
    
class A_info_UpdateView(LoginRequiredMixin,UpdateView):
    model=AdditionalInfo
    form_class=AdditionalInfoForm
    template_name='profile/create_ainfo.html'
    success_url=reverse_lazy('create_media')
    pk_url_kwarg = 'id'
    
    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
    
    
    
    
class UserMediaCreateView(LoginRequiredMixin, CreateView):
    model = UserMedia
    form_class = UserMediaForm
    template_name = 'profile/update_umedia.html'
    success_url = reverse_lazy('emp_status')

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class UserMediaUpdateView(LoginRequiredMixin, UpdateView):
    model = UserMedia
    form_class = UserMediaForm
    template_name = 'profile/update_umedia.html'
    success_url = reverse_lazy('index')

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_media'] = get_object_or_404(UserMedia, user=self.request.user, pk=self.kwargs['pk'])
        return context

    
class EmployeeinfoView(View,LoginRequiredMixin):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('signin')
        employee_form = EmployeeForm()
        jobseeker_form = JobseekerForm()
        return render(request, 'emp_status.html', {
            'employee_form': employee_form,
            'jobseeker_form': jobseeker_form
        })

    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('signin')
        if 'employee_submit' in request.POST:
            employee_form = EmployeeForm(request.POST)
            jobseeker_form = JobseekerForm()
            if employee_form.is_valid():
                employee = employee_form.save(commit=False)
                employee.user = request.user
                employee.save()
                return redirect('matches')
        elif 'jobseeker_submit' in request.POST:
            jobseeker_form = JobseekerForm(request.POST)
            employee_form = EmployeeForm()
            if jobseeker_form.is_valid():
                jobseeker = jobseeker_form.save(commit=False)
                jobseeker.user = request.user
                jobseeker.save()
                return redirect('matches')
        return render(request, 'emp_status.html', {
            'employee_form': employee_form,
            'jobseeker_form': jobseeker_form
        })




class Matches(LoginRequiredMixin, TemplateView):
    template_name = "matches.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_user = self.request.user
        current_user_district = current_user.personalinfo.district
        current_user_state = current_user.personalinfo.state
        current_user_qualification = current_user.personalinfo.qualification
        current_user_designation = current_user.personalinfo.designation
        
        # Filter users based on location
        location_filtered_users = Customuser.objects.filter(
            (Q(personalinfo__state=current_user_state) | 
             Q(personalinfo__district=current_user_district))
        ).exclude(id=current_user.id).exclude(id__in=current_user.hidden_profiles.all())

        # Filter users based on qualification and designation and exclude hidden profiles
        qualification_filtered_users = Customuser.objects.filter(
            (Q(personalinfo__qualification=current_user_qualification) | 
             Q(personalinfo__designation=current_user_designation))
        ).exclude(id=current_user.id).exclude(id__in=current_user.hidden_profiles.all())
        
        # Attach UserMedia to each user in location_filtered_users
        for user in location_filtered_users:
            user.user_media = UserMedia.objects.filter(user=user).first()
        
        # Attach UserMedia to each user in qualification_filtered_users
        for user in qualification_filtered_users:
            user.user_media = UserMedia.objects.filter(user=user).first()
        
        friend_requests= FriendRequest.objects.filter(to_user=self.request.user, status=False)
        
        context['location_filtered_users'] = location_filtered_users
        context['qualification_filtered_users'] = qualification_filtered_users
        context['friend_requests']=friend_requests
        
        return context
@login_required   
def hide_profile(request, user_id):
    user_to_hide = Customuser.objects.get(id=user_id)
    request.user.hidden_profiles.add(user_to_hide)
    return redirect('matches')  

@login_required
def like_profile(request, user_id):
    user_to_like = get_object_or_404(Customuser, id=user_id)
    if user_to_like != request.user:
        request.user.liked_profiles.add(user_to_like)
        user_to_like.liked_by_profiles.add(request.user)
        # Notify user_to_like here if necessary
    return redirect('matches')  

#friend request/accept/reject

@login_required
def send_friend_request(request, user_id):
    to_user = get_object_or_404(Customuser, id=user_id)
    friend_request, created = FriendRequest.objects.get_or_create(from_user=request.user, to_user=to_user)
    if created:
        # Friend request sent
        pass
    else:
        # Friend request was already sent
        pass
    return redirect('matches',)

@login_required
def accept_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id)
    if friend_request.to_user == request.user:
        friend_request.status = True
        friend_request.save()
        # Add each other as friends (you can implement this based on your app's needs)
    return redirect('friends')

@login_required
def reject_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id)
    if friend_request.to_user == request.user:
        friend_request.delete()
    return redirect('matches')

@login_required
def friends_list(request):
    friends = FriendRequest.objects.filter(
        (Q(from_user=request.user) | Q(to_user=request.user)),
        status=True
    )
    return render(request, 'friends.html', {'friends': friends})