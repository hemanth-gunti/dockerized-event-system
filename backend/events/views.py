from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import timedelta

from .models import Event, Enrollment
from .serializers import EventSerializer
from users.permissions import IsFacilitator, IsSeeker
from .tasks import send_followup_email, send_reminder_email


# -------------------------
# Facilitator: Create / Manage Events
# -------------------------
class EventViewSet(ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get_permissions(self):
        if self.request.method in ["POST", "PUT", "DELETE"]:
            return [IsAuthenticated(), IsFacilitator()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


# -------------------------
# Seeker: Enroll in Event
# -------------------------
class EnrollView(APIView):
    permission_classes = [IsAuthenticated, IsSeeker]

    def post(self, request, event_id):
        event = get_object_or_404(Event, id=event_id)

        # Prevent duplicate enrollment
        if Enrollment.objects.filter(event=event, seeker=request.user).exists():
            return Response({"detail": "Already enrolled"})

        # Check capacity
        if Enrollment.objects.filter(event=event, status="enrolled").count() >= event.capacity:
            return Response({"detail": "Event full"})

        # Create enrollment
        enrollment = Enrollment.objects.create(event=event, seeker=request.user)

        # Send confirmation email immediately
        send_followup_email.delay(enrollment.id)

        # Schedule reminder exactly 1 hour before event
        event_time = event.starts_at
        reminder_time = event_time - timedelta(hours=1)

        if reminder_time > timezone.now():
            send_reminder_email.apply_async(
                args=[enrollment.id],
                eta=reminder_time
            )

        return Response({"detail": "Enrolled successfully"})


# -------------------------
# Seeker: View My Enrollments
# -------------------------
class MyEnrollmentsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        now = timezone.now()

        upcoming = Enrollment.objects.filter(
            seeker=request.user,
            event__starts_at__gte=now
        )

        past = Enrollment.objects.filter(
            seeker=request.user,
            event__starts_at__lt=now
        )

        return Response({
            "upcoming": [
                {
                    "event": e.event.title,
                    "starts_at": e.event.starts_at
                } for e in upcoming
            ],
            "past": [
                {
                    "event": e.event.title,
                    "starts_at": e.event.starts_at
                } for e in past
            ]
        })
