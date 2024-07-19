from django.urls import path
from . import views

urlpatterns = [
    path('dashboard',views.dashboard,name="dashboard")
    # Add more paths as needed
]