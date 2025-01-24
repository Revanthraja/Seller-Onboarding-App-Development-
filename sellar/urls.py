from django.urls import path
from sellar import views
from django.contrib.auth import views as auth_views

urlpatterns = [
        path('', views.login_view, name='home'), # Added this
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('manufacturer_form/', views.manufacturer_form, name='manufacturer_form'),
    path('machine_vendor_form/', views.machine_vendor_form, name='machine_vendor_form'),
    path('professional_worker_form/', views.professional_worker_form, name='professional_worker_form'),
    path('profile/', views.profile_view, name='profile'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]