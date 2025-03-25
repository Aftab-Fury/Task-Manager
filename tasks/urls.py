from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api.views import TaskViewSet, UserTaskViewSet

router = DefaultRouter()
router.register(r'tasks', TaskViewSet)
router.register(r'users/(?P<user_id>\d+)/tasks', UserTaskViewSet, basename='user-tasks')

urlpatterns = [
    path('', include(router.urls)),
] 