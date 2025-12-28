from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import EventViewSet, EnrollView

router = DefaultRouter()
router.register('events', EventViewSet)

urlpatterns = router.urls

urlpatterns += [
    path('events/<int:event_id>/enroll/', EnrollView.as_view()),
]

from .views import MyEnrollmentsView

urlpatterns += [
    path('me/enrollments/', MyEnrollmentsView.as_view()),
]
