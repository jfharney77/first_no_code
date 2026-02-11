from django.urls import path
from . import views

app_name = 'chores'

urlpatterns = [
    # Calendar
    path('', views.calendar_view, name='calendar'),
    path('calendar/<int:year>/<int:month>/', views.calendar_view, name='calendar_month'),

    # Chores
    path('chore/add/', views.chore_create, name='chore_create'),
    path('chore/add/<str:date>/', views.chore_create, name='chore_create_date'),
    path('chore/<int:pk>/', views.chore_detail, name='chore_detail'),
    path('chore/<int:pk>/edit/', views.chore_update, name='chore_update'),
    path('chore/<int:pk>/delete/', views.chore_delete, name='chore_delete'),
    path('chore/<int:pk>/toggle/', views.chore_toggle_complete, name='chore_toggle'),

    # Recurring chores
    path('recurring/', views.recurring_list, name='recurring_list'),
    path('recurring/add/', views.recurring_create, name='recurring_create'),
    path('recurring/<int:pk>/edit/', views.recurring_update, name='recurring_update'),
    path('recurring/<int:pk>/delete/', views.recurring_delete, name='recurring_delete'),
    path('recurring/<int:pk>/generate/', views.recurring_generate, name='recurring_generate'),

    # Team members
    path('team/', views.team_member_list, name='team_list'),
    path('team/add/', views.team_member_create, name='team_create'),
    path('team/<int:pk>/edit/', views.team_member_update, name='team_update'),
    path('team/<int:pk>/delete/', views.team_member_delete, name='team_delete'),
]
