from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Event, Participant, Attendance

def index(request):
    """Home page view"""
    return render(request, 'attendance_app/index.html')

def event_list(request):
    """Display a list of events"""
    events = Event.objects.all().order_by('-date')
    return render(request, 'attendance_app/event_list.html', {'events': events})

def attendance_form(request, event_id):
    """Show attendance form for a specific event"""
    event = get_object_or_404(Event, pk=event_id)
    participants = Participant.objects.all().order_by('name')
    
    # Get existing attendance records
    attendance_records = Attendance.objects.filter(event=event)
    
    # Create a dictionary of participant ID -> present status
    attendance_data = {}
    for record in attendance_records:
        attendance_data[str(record.participant.id)] = record.present
    
    context = {
        'event': event,
        'participants': participants,
        'attendance_data_json': json.dumps(attendance_data),
    }
    return render(request, 'attendance_app/attendance_form.html', context)

@csrf_exempt  # For simplicity - use proper CSRF protection in production
def save_attendance(request, event_id):
    """API endpoint to save attendance data"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            event = get_object_or_404(Event, pk=event_id)
            
            for participant_id, is_present in data.items():
                participant = get_object_or_404(Participant, pk=int(participant_id))
                attendance, created = Attendance.objects.update_or_create(
                    event=event,
                    participant=participant,
                    defaults={'present': is_present}
                )
            
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)