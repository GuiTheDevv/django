from django.db import models
from django.utils import timezone

class Event(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateField(default=timezone.now)
    
    def __str__(self):
        return f"{self.name} ({self.date})"

class Participant(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    
    def __str__(self):
        return self.name

class Attendance(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    present = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['event', 'participant']
    
    def __str__(self):
        status = "Present" if self.present else "Absent"
        return f"{self.participant.name} - {self.event.name}: {status}"