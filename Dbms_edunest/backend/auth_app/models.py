from django.db import models
from django.utils.timezone import now

class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, unique=True)
    email = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=255) 
    class Meta:
        db_table = 'users' 
    def __str__(self):
        return self.username


class Note(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = 'notes'  # Name of the table in MySQL


class Reminder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    reminder_text = models.CharField(max_length=255)
    reminder_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'reminders'  # Name of the table in MySQL


# class UserAct(models.Model):  # Table to track user activity
#     user = models.OneToOneField(User, on_delete=models.CASCADE)  # Links to User
#     login_count = models.IntegerField(default=0) 
#     notes_access_count = models.IntegerField(default=0)  # How many times notes are accessed
#     last_login_at = models.DateTimeField(null=True, blank=True)  # Last login timestamp
#     last_activity_at = models.DateTimeField(auto_now=True)  # Last activity timestamp

#     class Meta:
#         db_table = 'user_act'  # Table name in MySQL

#     def __str__(self):
#         return f"{self.user.username} Activity"


class UserAct(models.Model):  
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Allows multiple logs per user
    activity_type = models.CharField(max_length=50)  # "LOGIN" or "NOTE_CREATION"
    last_activity_at = models.DateTimeField(auto_now=True)  # When the event occurred

    class Meta:
        db_table = 'user_act'  # Table name in MySQL

    def __str__(self):
        return f"{self.user.username} - {self.activity_type} at {self.timestamp}"


from django.db import models
from django.contrib.auth.models import User

class StudySession(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Foreign key to User model
    task = models.CharField(max_length=255)  # Task Name
    start_time = models.DateTimeField()  # Task Start Time
    end_time = models.DateTimeField()  # Task End Time
    session_date = models.DateField()  # Task Date
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp of Creation

    class Meta:
        db_table = 'study_sessions'  # MySQL table name

    def __str__(self):
        return f"{self.task} ({self.session_date})"

