# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from .models import Student

def student_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            student = Student.objects.get(username=username)
            # Check hashed password
            if check_password(password, student.password):
                request.session['student_id'] = student.id
                request.session['student_name'] = student.name
                return redirect('dashboard')
            else:
                return render(request, 'myauth/login.html', {
                    'error': 'Invalid username/password'
                })
        except Student.DoesNotExist:
            return render(request, 'myauth/login.html', {
                'error': 'Invalid username/password'
            })

    return render(request, 'myauth/login.html')


def dashboard(request):
    # Check if student is logged in
    if 'student_id' not in request.session:
        return redirect('login')

    student_name = request.session.get('student_name')
    return render(request, 'myauth/dashboard.html', {'name': student_name})


def logout(request):
    # Clear session
    request.session.flush()
    return redirect('login')
