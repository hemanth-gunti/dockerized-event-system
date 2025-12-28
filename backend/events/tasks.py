from celery import shared_task
from django.core.mail import send_mail
from .models import Enrollment

@shared_task
def send_followup_email(enrollment_id):
    enrollment = Enrollment.objects.get(id=enrollment_id)
    send_mail(
        "Thanks for enrolling",
        f"You enrolled in {enrollment.event.title}",
        "noreply@ahoum.com",
        [enrollment.seeker.email]
    )

@shared_task
def send_reminder_email(enrollment_id):
    enrollment = Enrollment.objects.get(id=enrollment_id)
    send_mail(
        "Event Reminder",
        f"Your event {enrollment.event.title} starts in 1 hour",
        "noreply@ahoum.com",
        [enrollment.seeker.email]
    )
