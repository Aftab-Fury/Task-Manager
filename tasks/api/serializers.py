from rest_framework import serializers
from django.contrib.auth.models import User
from ..models import Task

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model.
    Provides basic user information without sensitive data.
    """
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')
        read_only_fields = fields

class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for Task model.
    Handles task creation, updates, and provides nested user information.
    """
    assigned_to = UserSerializer(many=True, read_only=True)
    created_by = UserSerializer(read_only=True)
    assigned_to_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        write_only=True,
        queryset=User.objects.all(),
        source='assigned_to',
        required=False
    )

    class Meta:
        model = Task
        fields = (
            'id', 'name', 'description', 'created_at', 'task_type',
            'completed_at', 'status', 'assigned_to', 'created_by',
            'assigned_to_ids'
        )
        read_only_fields = ('created_at', 'completed_at')

    def validate_name(self, value):
        """Ensure task name is not too short."""
        if len(value.strip()) < 3:
            raise serializers.ValidationError("Task name must be at least 3 characters long.")
        return value.strip()

    def validate_status(self, value):
        """Validate status transitions."""
        if self.instance and self.instance.status == 'completed' and value != 'completed':
            raise serializers.ValidationError("Cannot change status of a completed task.")
        return value 