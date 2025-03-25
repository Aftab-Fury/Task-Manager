from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from ..models import Task

class TaskAPITest(APITestCase):
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
        
        # Set up API client
        self.client = APIClient()
        self.client.force_authenticate(user=self.user1)

    def test_create_task(self):
        """Test creating a new task"""
        url = reverse('task-list')
        data = {
            'name': 'New Task',
            'description': 'New Description',
            'task_type': 'testing',
            'status': 'pending'
        }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 2)
        self.assertEqual(Task.objects.get(name='New Task').created_by, self.user1)

    def test_list_tasks(self):
        """Test listing all tasks"""
        url = reverse('task-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Test Task')

    def test_get_task_detail(self):
        """Test getting task details"""
        url = reverse('task-detail', kwargs={'pk': self.task.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Task')
        self.assertEqual(response.data['description'], 'Test Description')

    def test_update_task(self):
        """Test updating a task"""
        url = reverse('task-detail', kwargs={'pk': self.task.pk})
        data = {
            'name': 'Updated Task',
            'status': 'in_progress'
        }
        
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated Task')
        self.assertEqual(response.data['status'], 'in_progress')

    def test_delete_task(self):
        """Test deleting a task"""
        url = reverse('task-detail', kwargs={'pk': self.task.pk})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)

    def test_assign_task(self):
        """Test assigning task to users"""
        url = reverse('task-assign', kwargs={'pk': self.task.pk})
        data = {'user_ids': [self.user2.id]}
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['assigned_to']), 1)
        self.assertEqual(response.data['assigned_to'][0]['id'], self.user2.id)

    def test_get_task_assignments(self):
        """Test getting task assignments"""
        self.task.assigned_to.add(self.user2)
        url = reverse('task-assignments', kwargs={'pk': self.task.pk})
        
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], self.user2.id)

    def test_get_user_tasks(self):
        """Test getting tasks assigned to a user"""
        self.task.assigned_to.add(self.user2)
        url = reverse('user-tasks-list', kwargs={'user_id': self.user2.id})
        
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], self.task.id)

    def test_unauthorized_access(self):
        """Test unauthorized access to API endpoints"""
        self.client.force_authenticate(user=None)
        url = reverse('task-list')
        
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_invalid_task_assignment(self):
        """Test assigning task with invalid user IDs"""
        url = reverse('task-assign', kwargs={'pk': self.task.pk})
        data = {'user_ids': [999]}  # Non-existent user ID
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST) 