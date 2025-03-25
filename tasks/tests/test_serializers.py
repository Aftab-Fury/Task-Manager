from django.test import TestCase
from django.contrib.auth.models import User
from ..models import Task
from ..api.serializers import TaskSerializer, UserSerializer

class SerializerTest(TestCase):
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
        self.task.assigned_to.add(self.user2)

    def test_user_serializer(self):
        """Test UserSerializer serialization"""
        serializer = UserSerializer(self.user1)
        data = serializer.data
        
        self.assertEqual(data['id'], self.user1.id)
        self.assertEqual(data['username'], 'testuser1')
        self.assertEqual(data['email'], 'test1@example.com')

    def test_task_serializer(self):
        """Test TaskSerializer serialization"""
        serializer = TaskSerializer(self.task)
        data = serializer.data
        
        self.assertEqual(data['id'], self.task.id)
        self.assertEqual(data['name'], 'Test Task')
        self.assertEqual(data['description'], 'Test Description')
        self.assertEqual(data['task_type'], 'Development')
        self.assertEqual(data['status'], 'pending')
        self.assertEqual(len(data['assigned_to']), 1)
        self.assertEqual(data['created_by']['id'], self.user1.id)

    def test_task_serializer_create(self):
        """Test TaskSerializer deserialization and creation"""
        data = {
            'name': 'New Task',
            'description': 'New Description',
            'task_type': 'testing',
            'assigned_to_ids': [self.user1.id]
        }
        serializer = TaskSerializer(data=data, partial=True)
        self.assertTrue(serializer.is_valid())
        
        task = serializer.save(created_by=self.user2)
        self.assertEqual(task.name, 'New Task')
        self.assertEqual(task.description, 'New Description')
        self.assertEqual(task.task_type, 'testing')
        self.assertEqual(task.created_by, self.user2)
        self.assertEqual(task.assigned_to.count(), 1)
        self.assertIn(self.user1, task.assigned_to.all())

    def test_task_serializer_update(self):
        """Test TaskSerializer update"""
        data = {
            'name': 'Updated Task',
            'status': 'in_progress'
        }
        serializer = TaskSerializer(self.task, data=data, partial=True)
        self.assertTrue(serializer.is_valid())
        
        task = serializer.save()
        self.assertEqual(task.name, 'Updated Task')
        self.assertEqual(task.status, 'in_progress')
        # Check that other fields remain unchanged
        self.assertEqual(task.description, 'Test Description')
        self.assertEqual(task.task_type, 'Development') 