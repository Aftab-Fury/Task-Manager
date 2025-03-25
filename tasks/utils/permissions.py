from rest_framework import permissions

class IsTaskCreatorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow creators of a task to edit it.
    Read-only access is allowed for other authenticated users.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed for any authenticated request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the creator of the task
        return obj.created_by == request.user 