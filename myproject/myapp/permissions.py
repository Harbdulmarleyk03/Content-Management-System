from rest_framework.permissions import BasePermission

class CanPublishPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.groups.filter(name="Editor").exists()
    

class IsAuthorOrEditor(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.groups.filter(name="Editors").exists():
            return True
        return obj.author == request.user 