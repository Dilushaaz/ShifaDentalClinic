from django.shortcuts import render
from django.db.models import Sum
from .models import Patient, Appointment, Expense
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from django.http import FileResponse
import io

def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


def register(request):

    if request.method == 'POST':

        Patient.objects.create(
            name=request.POST['name'],
            age=request.POST['age'],
            gender=request.POST['gender'],
            phone=request.POST['phone'],
            address=request.POST['address']
        )

    return render(request, 'register.html')


def patient_list(request):

    search = request.GET.get('search')

    if search:
        patients = Patient.objects.filter(
            name__icontains=search
        )
    else:
        patients = Patient.objects.all()

    return render(
        request,
        'patient_list.html',
        {'patients': patients}
    )


def appointment(request):

    if request.method == 'POST':

        patient = Patient.objects.get(
            id=request.POST['patient']
        )

        Appointment.objects.create(
            patient=patient,
            date=request.POST['date'],
            time=request.POST['time'],
            treatment=request.POST['treatment'],
            fee=request.POST['fee']
        )

    patients = Patient.objects.all()

    return render(
        request,
        'appointment.html',
        {'patients': patients}
    )


def appointment_list(request):

    appointments = Appointment.objects.all()

    return render(
        request,
        'appointment_list.html',
        {'appointments': appointments}
    )


def expense(request):

    if request.method == 'POST':

        Expense.objects.create(
            title=request.POST['title'],
            amount=request.POST['amount'],
            date=request.POST['date']
        )

    return render(request, 'expense.html')


def expense_list(request):

    expenses = Expense.objects.all()

    return render(
        request,
        'expense_list.html',
        {'expenses': expenses}
    )


@login_required
def dashboard(request):

    total_income = Appointment.objects.aggregate(
        Sum('fee')
    )['fee__sum'] or 0

    total_expense = Expense.objects.aggregate(
        Sum('amount')
    )['amount__sum'] or 0

    net_profit = total_income - total_expense

    context = {
        'income': total_income,
        'expense': total_expense,
        'profit': net_profit
    }

    return render(
        request,
        'dashboard.html',
        context
    )
def login_view(request):

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:
            login(request, user)
            return redirect('/dashboard')

    return render(request, 'login.html')
def logout_view(request):
    logout(request)
    return redirect('/login')
def weekly_report(request):

    total_income = Appointment.objects.aggregate(
        Sum('fee')
    )['fee__sum'] or 0

    total_expense = Expense.objects.aggregate(
        Sum('amount')
    )['amount__sum'] or 0

    profit = total_income - total_expense

    buffer = io.BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph(
            "Shifa Dental Clinic - Weekly Report",
            styles['Title']
        )
    )

    content.append(Spacer(1, 12))

    content.append(
        Paragraph(
            "Doctor: Dr. Anees VP",
            styles['Normal']
        )
    )

    content.append(
        Paragraph(
            f"Total Income: ₹{total_income}",
            styles['Normal']
        )
    )

    content.append(
        Paragraph(
            f"Total Expense: ₹{total_expense}",
            styles['Normal']
        )
    )

    content.append(
        Paragraph(
            f"Net Profit: ₹{profit}",
            styles['Normal']
        )
    )

    doc.build(content)

    buffer.seek(0)

    return FileResponse(
        buffer,
        as_attachment=True,
        filename='Weekly_Report.pdf'
    )

def monthly_report(request):

    buffer = io.BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph(
            "Shifa Dental Clinic - Monthly Report",
            styles['Title']
        )
    )

    doc.build(content)

    buffer.seek(0)

    return FileResponse(
        buffer,
        as_attachment=True,
        filename='Monthly_Report.pdf'
    )


def annual_report(request):

    buffer = io.BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph(
            "Shifa Dental Clinic - Annual Report",
            styles['Title']
        )
    )

    doc.build(content)

    buffer.seek(0)

    return FileResponse(
        buffer,
        as_attachment=True,
        filename='Annual_Report.pdf'
    )
def edit_patient(request, id):

    patient = Patient.objects.get(id=id)

    if request.method == 'POST':

        patient.name = request.POST['name']
        patient.age = request.POST['age']
        patient.gender = request.POST['gender']
        patient.phone = request.POST['phone']
        patient.address = request.POST['address']

        patient.save()

        return redirect('/patients')

    return render(
        request,
        'edit_patient.html',
        {'patient': patient}
    )


def delete_patient(request, id):

    patient = Patient.objects.get(id=id)

    patient.delete()

    return redirect('/patients')
def delete_appointment(request, id):

    appointment = Appointment.objects.get(id=id)

    appointment.delete()

    return redirect('/appointments')
def delete_expense(request, id):

    expense = Expense.objects.get(id=id)

    expense.delete()

    return redirect('/expenses')