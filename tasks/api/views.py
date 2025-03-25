from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from ..models import Task
from .serializers import TaskSerializer, UserSerializer
from ..utils.permissions import IsTaskCreatorOrReadOnly

class TaskViewSet(viewsets.ModelViewSet):
    """ViewSet for managing tasks with CRUD operations and task assignments."""
    
    queryset = Task.objects.select_related('created_by').prefetch_related('assigned_to').all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsTaskCreatorOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        status = self.request.query_params.get('status')
        task_type = self.request.query_params.get('task_type')

        if status:
            queryset = queryset.filter(status=status)
        if task_type:
            queryset = queryset.filter(task_type=task_type)

        return queryset

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @swagger_auto_schema(
        method='post',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'user_ids': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(type=openapi.TYPE_INTEGER),
                    description='List of user IDs to assign to the task'
                )
            },
            required=['user_ids']
        ),
        responses={
            200: TaskSerializer,
            400: 'Bad Request',
            404: 'Not Found'
        }
    )
    @action(detail=True, methods=['post'])
    def assign(self, request, pk=None):
        task = self.get_object()
        user_ids = request.data.get('user_ids', [])
        
        if not user_ids:
            return Response(
                {'error': 'No user IDs provided'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        users = User.objects.filter(id__in=user_ids)
        if not users.exists() or users.count() != len(user_ids):
            return Response(
                {'error': 'Invalid user IDs provided'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        task.assigned_to.set(users)
        return Response(self.get_serializer(task).data)

    @swagger_auto_schema(
        responses={
            200: UserSerializer(many=True),
            404: 'Not Found'
        }
    )
    @action(detail=True, methods=['get'])
    def assignments(self, request, pk=None):
        task = self.get_object()
        return Response(UserSerializer(task.assigned_to.all(), many=True).data)

class UserTaskViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for retrieving tasks assigned to a specific user."""
    
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Handle schema generation case
        if getattr(self, 'swagger_fake_view', False):
            return Task.objects.none()
            
        return Task.objects.filter(
            assigned_to__id=self.kwargs['user_id']
        ).select_related('created_by').prefetch_related('assigned_to') 