from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api.views import TaskViewSet, UserTaskViewSet, UserNameTaskList

router = DefaultRouter()
router.register(r'tasks', TaskViewSet)
router.register(r'users/(?P<user_id>\d+)/tasks', UserTaskViewSet, basename='user-tasks')

urlpatterns = [
    path('', include(router.urls)),
    # Username-based tasks endpoint for convenience: /api/users/<username>/tasks/
    path('users/<str:username>/tasks/', UserNameTaskList.as_view(), name='user-tasks-by-username'),
] 