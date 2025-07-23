from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth import get_user_model

from django.contrib.auth import authenticate, login

from .models import Assignment,Submission,User
from django.contrib.auth.decorators import login_required


from datetime import datetime

from django.shortcuts import render


User = get_user_model()

def authenticate_user(username):
    try:
        return User.objects.get(username=username)
    except User.DoesNotExist:
        return None





@csrf_exempt
def signup_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        role = data.get('role')  # 'student' or 'teacher'

        if not username or not password or role not in ['student', 'teacher']:
            return JsonResponse({'error': 'Invalid data'}, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username already exists'}, status=400)

        user = User.objects.create_user(username=username, password=password, role=role)
        return JsonResponse({'message': 'User created successfully'})
    else:
        return JsonResponse({'error': 'Only POST allowed'}, status=405)
    

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return JsonResponse({'message': 'Login successful', 'role': user.role})
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=400)
    else:
        return JsonResponse({'error': 'Only POST allowed'}, status=405)



@csrf_exempt
def create_assignment(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User does not exist'}, status=404)

        if user.role != 'teacher':
            return JsonResponse({'error': 'Only teachers can create assignments'}, status=403)

        title = data.get('title')
        description = data.get('description')
        due_date = data.get('due_date')

        if not title or not due_date:
            return JsonResponse({'error': 'Missing fields'}, status=400)

        Assignment.objects.create(
            title=title,
            description=description,
            due_date=due_date,
            teacher=user
        )

        return JsonResponse({'message': 'Assignment created successfully'})

    return JsonResponse({'error': 'Only POST allowed'}, status=405)



@csrf_exempt
def submit_assignment(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        assignment_id = request.POST.get('assignment_id')
        submitted_file = request.FILES.get('submitted_file')

        # Check user exists
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)

        # Check user is a student
        if user.role != 'student':
            return JsonResponse({'error': 'Only students can submit assignments'}, status=403)

        # Check assignment exists
        try:
            assignment = Assignment.objects.get(id=assignment_id)
        except Assignment.DoesNotExist:
            return JsonResponse({'error': 'Assignment not found'}, status=404)

        # Create submission
        Submission.objects.create(
            assignment=assignment,
            student=user,
            submitted_file=submitted_file
        )

        return JsonResponse({'message': 'Submission successful'})
    else:
        return JsonResponse({'error': 'Only POST allowed'}, status=405)
    






@csrf_exempt
def view_submissions(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        assignment_id = data.get('assignment_id')

        try:
            user = User.objects.get(username=username)
            if user.role != 'teacher':
                return JsonResponse({'error': 'Only teachers can view submissions'}, status=403)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User does not exist'}, status=404)

        try:
            assignment = Assignment.objects.get(id=assignment_id, teacher=user)
        except Assignment.DoesNotExist:
            return JsonResponse({'error': 'Assignment not found or not owned by teacher'}, status=404)

        submissions = Submission.objects.filter(assignment=assignment)

        result = []
        for sub in submissions:
            result.append({
                'student': sub.student.username,
                'submitted_at': sub.submitted_at.isoformat(),
                'submitted_file_url': request.build_absolute_uri(sub.submitted_file.url)
            })

        return JsonResponse({'submissions': result})

    return JsonResponse({'error': 'Only POST allowed'}, status=405)



def frontend_create(request):
    return render(request, "create_assignment.html")

def frontend_submit(request):
    return render(request, "submit_assignment.html")

def frontend_view(request):
    return render(request, "view_submissions.html")
