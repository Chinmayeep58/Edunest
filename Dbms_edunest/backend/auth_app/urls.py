from django.urls import path
from . import views

urlpatterns = [
    
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile_view, name='profile'),
    path('logout/', views.logout_view, name='logout'),
    
    # Add this:
    path('mynotes/', views.mynotes_view, name='mynotes'),
    path('studyplanner/', views.studyplanner_view, name='studyplanner'),
    path('focus/', views.focus_view, name='focus'),
    path('reminder/', views.reminder_view, name='reminder'),

    path('save_note/', views.save_note, name='save_note'),  # Example URL
    path('notes/', views.notes_list, name='notes'),

    path("save-reminder/", views.save_reminder, name="save_reminder"),
    path("get-reminders/", views.get_reminders, name="get_reminders"),
    path("auth/delete-reminder/<int:reminder_id>/", views.delete_reminder, name="delete_reminder"),

]
