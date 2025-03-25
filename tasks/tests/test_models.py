from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from ..models import Task

class TaskModelTest(TestCase):
    def setUp(self):
        # Create test users
        self.user1 = User.objects.create_user(
            username='testuser1',
            email='test1@example.com',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='testpass123'
        )
        
        # Create a test task
        self.task = Task.objects.create(
            name='Test Task',
            description='Test Description',
            task_type='Development',
            created_by=self.user1
        )

    def test_task_creation(self):
        """Test if a task can be created with all required fields"""
        self.assertEqual(self.task.name, 'Test Task')
        self.assertEqual(self.task.description, 'Test Description')
        self.assertEqual(self.task.task_type, 'Development')
        self.assertEqual(self.task.status, 'pending')
        self.assertIsNone(self.task.completed_at)
        self.assertEqual(self.task.created_by, self.user1)

    def test_task_status_update(self):
        """Test if task status can be updated"""
        self.task.status = 'in_progress'
        self.task.save()
        self.assertEqual(self.task.status, 'in_progress')

    def test_task_completion(self):
        """Test if task completion can be recorded"""
        self.task.status = 'completed'
        self.task.completed_at = timezone.now()
        self.task.save()
        self.assertEqual(self.task.status, 'completed')
        self.assertIsNotNone(self.task.completed_at)

    def test_task_assignment(self):
        """Test if task can be assigned to multiple users"""
        self.task.assigned_to.add(self.user1, self.user2)
        self.assertEqual(self.task.assigned_to.count(), 2)
        self.assertIn(self.user1, self.task.assigned_to.all())
        self.assertIn(self.user2, self.task.assigned_to.all())

    def test_task_string_representation(self):
        """Test the string representation of the task"""
        self.assertEqual(str(self.task), 'Test Task') 