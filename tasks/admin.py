from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'task_type', 'status', 'created_by',
        'created_at', 'completed_at', 'get_assigned_users'
    )
    list_filter = ('status', 'task_type', 'created_at', 'completed_at')
    search_fields = ('name', 'description', 'created_by__username', 'assigned_to__username')
    filter_horizontal = ('assigned_to',)
    readonly_fields = ('created_at', 'completed_at')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'task_type')
        }),
        ('Status', {
            'fields': ('status', 'created_at', 'completed_at')
        }),
        ('Assignment', {
            'fields': ('created_by', 'assigned_to')
        }),
    )

    def get_assigned_users(self, obj):
        return ", ".join(user.username for user in obj.assigned_to.all())
    get_assigned_users.short_description = 'Assigned To'

    def save_model(self, request, obj, form, change):
        if not change and not obj.created_by:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
