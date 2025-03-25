from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Task(models.Model):
    """Task model for managing user assignments and task states."""
    
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        IN_PROGRESS = 'in_progress', 'In Progress'
        COMPLETED = 'completed', 'Completed'

    class TaskType(models.TextChoices):
        DEVELOPMENT = 'development', 'Development'
        TESTING = 'testing', 'Testing'
        DOCUMENTATION = 'documentation', 'Documentation'
        DEPLOYMENT = 'deployment', 'Deployment'
        OTHER = 'other', 'Other'

    name = models.CharField(max_length=200, help_text="Name of the task")
    description = models.TextField(help_text="Detailed description of the task")
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the task was created")
    task_type = models.CharField(
        max_length=20,
        choices=TaskType.choices,
        default=TaskType.OTHER,
        help_text="Type of the task"
    )
    completed_at = models.DateTimeField(null=True, blank=True, help_text="When the task was completed")
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        help_text="Current status of the task"
    )
    assigned_to = models.ManyToManyField(
        User,
        related_name='assigned_tasks',
        blank=True,
        help_text="Users assigned to this task"
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_tasks',
        help_text="User who created the task"
    )

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['task_type']),
            models.Index(fields=['created_at']),
        ]
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """
        Override save method to handle task completion logic.
        Sets completed_at timestamp when task is marked as completed.
        """
        if self.status == self.Status.COMPLETED and not self.completed_at:
            self.completed_at = timezone.now()
        elif self.status != self.Status.COMPLETED:
            self.completed_at = None
        super().save(*args, **kwargs)

    @property
    def is_completed(self):
        """Check if the task is completed."""
        return self.status == self.Status.COMPLETED

    @property
    def duration(self):
        """Calculate the duration of the task if completed."""
        return self.completed_at - self.created_at if self.completed_at else None
