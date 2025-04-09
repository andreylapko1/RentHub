from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission

from bookings.models import Booking


class IsLandlord(BasePermission):
    def has_object_permission(self, request, view, obj):
        # if request.method in permissions.SAFE_METHODS:
        #     return True
        return request.user == obj.landlord


class IsLandlordEmail(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.email == obj.landlord_email


class IsLandlordOrForbidden(BasePermission):
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Booking):
            if obj.landlord_email == request.user.email:
                return True
            else:
                if request.method == 'GET':
                    raise PermissionDenied('You do not have permission to view this booking.')
                return False
        return False
