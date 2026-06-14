from django.urls import path
from . import views
from django.shortcuts import render, redirect
from .models import Patient, Appointment, Expense

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('register/', views.register, name='register'),
    path('appointment/', views.appointment, name='appointment'),
    path(
    'appointments/',
    views.appointment_list,
    name='appointments'
),
    path('expense/', views.expense, name='expense'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('patients/', views.patient_list, name='patients'),
    path(
    'expenses/',
    views.expense_list,
    name='expenses'
),
path('login/', views.login_view, name='login'),
path('logout/', views.logout_view, name='logout'),
path('weekly-report/', views.weekly_report),
path('monthly-report/', views.monthly_report),
path('annual-report/', views.annual_report),
path(
    'edit-patient/<int:id>/',
    views.edit_patient,
    name='edit_patient'
),
path(
    'delete-patient/<int:id>/',
    views.delete_patient,
    name='delete_patient'
),
path(
    'delete-appointment/<int:id>/',
    views.delete_appointment,
    name='delete_appointment'
),
path(
    'delete-expense/<int:id>/',
    views.delete_expense,
    name='delete_expense'
),
]
