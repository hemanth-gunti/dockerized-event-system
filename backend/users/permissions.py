from rest_framework.permissions import BasePermission

class IsFacilitator(BasePermission):
    def has_permission(self, request, view):
        return request.user.profile.role == 'facilitator'

class IsSeeker(BasePermission):
    def has_permission(self, request, view):
        return request.user.profile.role == 'seeker'
