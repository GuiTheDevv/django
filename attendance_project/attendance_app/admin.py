from django.contrib import admin
from .models import Event, Participant, Attendance

admin.site.register(Event)
admin.site.register(Participant)
admin.site.register(Attendance)