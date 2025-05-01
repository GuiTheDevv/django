from django.urls import path
from . import views

app_name = 'attendance_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('events/', views.event_list, name='event_list'),
    path('events/<int:event_id>/', views.attendance_form, name='attendance_form'),
    path('events/<int:event_id>/save/', views.save_attendance, name='save_attendance'),
]