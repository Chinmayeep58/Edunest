from django.shortcuts import render, redirect
from django.db import connection
from .forms import RegisterForm, LoginForm
import hashlib
import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Note
from django.utils import timezone
import datetime

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", 
                               [username, email, hashed_password])

            return redirect('login')
    else:
        form = RegisterForm()
    
    return render(request, 'auth_app/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", 
                               [username, hashed_password])
                user = cursor.fetchone()

            if user:
                request.session['username'] = username  # Store session data
                return redirect('dashboard')
            else:
                return render(request, 'auth_app/login.html', {'form': form, 'error': 'Invalid Credentials'})
    
    else:
        form = LoginForm()

    return render(request, 'auth_app/login.html', {'form': form})


def dashboard(request):
    if 'username' not in request.session:
        return redirect('login')

    return render(request, 'auth_app/dashboard.html', {'username': request.session['username']})


def logout_view(request):
    request.session.flush()
    return redirect('login')

def profile_view(request):
    return render(request, 'auth_app/profile.html')  # Create a profile.html file


def mynotes_view(request):
    return render(request, 'auth_app/mynotes.html')

def studyplanner_view(request):
    return render(request, 'auth_app/studyplanner.html')

def focus_view(request):
    return render(request, 'auth_app/focus.html')


def reminder_view(request):
    return render(request, 'auth_app/reminder.html')


@csrf_exempt
def save_note(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        username = request.session.get('username')  # Retrieve the logged-in user

        if title and content and username:
            with connection.cursor() as cursor:
                # Fetch the user ID from the database
                cursor.execute("SELECT id FROM users WHERE username = %s", [username])
                user = cursor.fetchone()

                if user:
                    user_id = user[0]

                    # Insert the note into the notes table
                    cursor.execute("""
                        INSERT INTO notes (user_id, title, content, created_at) 
                        VALUES (%s, %s, %s, NOW())
                    """, [user_id, title, content])

                    cursor.execute("""
                    INSERT INTO user_act (user_id, login_count, notes_access_count, last_activity_at) 
                    VALUES (%s, 0, 1, %s)
                    ON DUPLICATE KEY UPDATE 
                        notes_access_count = notes_access_count + 1, 
                        last_activity_at = %s
                """, [user_id, now(), now()])

                    return redirect("notes")  # Redirect to the notes page

    return render(request, "notes_app/mynotes.html")

def notes_view(request):
    username = request.session.get('username')

    if username:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id FROM users WHERE username = %s", [username])
            user = cursor.fetchone()

            if user:
                user_id = user[0]

                # Increment notes access count
                cursor.execute("""
                INSERT INTO user_act (user_id, notes_access_count, last_activity_at) 
                VALUES (%s, 1, %s)
                ON DUPLICATE KEY UPDATE 
                    notes_access_count = notes_access_count + 1, 
                    last_activity_at = %s
            """, [user_id, now(), now()])

                # Fetch notes for the logged-in user
                cursor.execute("SELECT title, content, created_at FROM notes WHERE user_id = %s ORDER BY created_at DESC", [user_id])
                notes = cursor.fetchall()

                notes_list = [{'title': note[0], 'content': note[1], 'created_at': note[2]} for note in notes]

                return render(request, "notes_app/mynotes.html", {'notes': notes_list})

    return redirect('login')


def notes_list(request):
    notes = Note.objects.all()
    return render(request, "auth_app/mynotes.html", {"notes": notes})



def profile_view(request):
    username = request.session.get('username')  # Get the logged-in user

    if username:
        with connection.cursor() as cursor:
            cursor.execute("SELECT username, email FROM users WHERE username = %s", [username])
            user = cursor.fetchone()

        if user:
            user_data = {
                "username": user[0],
                "email": user[1],
                # "current_task": user[2] if user[2] else "No current task",
                # "completed_tasks": user[3] if user[3] else "0",
                # "usage_time": user[4] if user[4] else "0 mins"
            }
        else:
            user_data = {}

        return render(request, "auth_app/profile.html", {"user": user_data})

    return redirect("login")  # Redirect to login if no session



import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Reminder
from django.contrib.auth.models import User

@csrf_exempt
def save_reminder(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user = User.objects.first()  # Replace this with the logged-in user logic
            reminder = Reminder.objects.create(
                user=user,
                reminder_text=data["reminder_text"],
                reminder_time=data["reminder_time"]
            )
            return JsonResponse({"message": "Reminder saved successfully!", "id": reminder.id})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

def get_reminders(request):
    reminders = Reminder.objects.all().values("reminder_text", "reminder_time")
    return JsonResponse({"reminders": list(reminders)})


def get_reminders(request):
    """Fetches reminders from the database for the logged-in user."""
    username = request.session.get("username")

    if username:
        with connection.cursor() as cursor:
            # MySQL Query to fetch user ID based on the session username
            query_get_user_id = "SELECT id FROM users WHERE username = %s"
            cursor.execute(query_get_user_id, [username])
            user = cursor.fetchone()

            if user:
                user_id = user[0]

                # MySQL Query to fetch reminders for the specific user
                query_get_reminders = """
                    SELECT id, reminder_text, reminder_time 
                    FROM reminders 
                    WHERE user_id = %s 
                    ORDER BY reminder_time ASC
                """
                cursor.execute(query_get_reminders, [user_id])
                reminders = cursor.fetchall()

                # Formatting the result into JSON response
                reminders_list = [
                    {"id": r[0], "text": r[1], "time": str(r[2])} for r in reminders
                ]
                return JsonResponse({"reminders": reminders_list})

    return JsonResponse({"reminders": []})


from django.utils.timezone import make_aware, is_naive, get_current_timezone
from datetime import datetime
import json

def save_reminder(request):
    """Saves a new reminder for the logged-in user."""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            reminder_text = data.get("reminder_text")
            reminder_time_str = data.get("reminder_time")  # Example: '2025-02-14T10:10:00.000Z'

            print(f"Received Reminder Text: {reminder_text}")
            print(f"Received Reminder Time (String): {reminder_time_str}")

            # Convert string to datetime object
            reminder_time = datetime.fromisoformat(reminder_time_str.replace("Z", ""))

            # Convert to correct timezone before saving
            if is_naive(reminder_time):  
                reminder_time = make_aware(reminder_time, timezone=get_current_timezone())

            username = request.session.get("username")

            if username:
                with connection.cursor() as cursor:
                    # Get user ID from username
                    cursor.execute("SELECT id FROM users WHERE username = %s", [username])
                    user = cursor.fetchone()

                    if user:
                        user_id = user[0]

                        # Insert reminder into the database with the correct timezone
                        cursor.execute("""
                            INSERT INTO reminders (user_id, reminder_text, reminder_time, created_at) 
                            VALUES (%s, %s, %s, NOW())
                        """, [user_id, reminder_text, reminder_time])

                        return JsonResponse({"message": "Reminder saved successfully!"})

            return JsonResponse({"error": "User not found!"}, status=400)

        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request method!"}, status=405)


from django.http import JsonResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from .models import Reminder

@csrf_exempt
def delete_reminder(request, reminder_id):
    """Deletes a reminder by ID for the logged-in user."""
    if request.method == "DELETE":
        username = request.session.get("username")

        if username:
            with connection.cursor() as cursor:
                # Get user ID from username
                cursor.execute("SELECT id FROM users WHERE username = %s", [username])
                user = cursor.fetchone()

                if user:
                    user_id = user[0]

                    # Check if the reminder exists and belongs to the user
                    cursor.execute("""
                        SELECT id FROM reminders WHERE id = %s AND user_id = %s
                    """, [reminder_id, user_id])
                    reminder = cursor.fetchone()

                    if reminder:
                        # Delete the reminder
                        cursor.execute("DELETE FROM reminders WHERE id = %s", [reminder_id])
                        return JsonResponse({"message": "Reminder deleted successfully!"})
                    else:
                        return JsonResponse({"error": "Reminder not found or unauthorized!"}, status=403)

        return JsonResponse({"error": "User not found!"}, status=400)

    return JsonResponse({"error": "Invalid request method!"}, status=405)


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.db import connection
from django.utils.timezone import now
from .models import User, UserAct

def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            current_time = now()

            # Log user login activity
            with connection.cursor() as cursor:
                cursor.execute("SELECT id FROM users WHERE username = %s", [username])
                user_id = cursor.fetchone()[0]

                cursor.execute("SELECT * FROM user_act WHERE user_id = %s", [user_id])
                user_act = cursor.fetchone()

                cursor.execute("""
                    INSERT INTO user_act (user_id, login_count, notes_access_count, last_login_at, last_activity_at) 
                    VALUES (%s, 1, 0, %s, %s)
                    ON DUPLICATE KEY UPDATE 
                        login_count = login_count + 1, 
                        last_login_at = %s, 
                        last_activity_at = %s;
                """, [user.id, current_time, current_time, current_time, current_time])

            return redirect("dashboard")

    return render(request, "auth_app/login.html")
