from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from apps.queue.models import Region, Office, Counter, QueueTicket


class TicketAPITestCase(TestCase):
    """Test ticket API endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.region = Region.objects.create(name='Dar es Salaam')
        self.office = Office.objects.create(name='Main Office', region=self.region)
        self.counter = Counter.objects.create(name='Counter 1', office=self.office)
    
    def test_create_ticket(self):
        response = self.client.post('/api/tickets/', {
            'region_id': self.region.id,
            'office_id': self.office.id
        }, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('ticket_number', response.data)
        self.assertEqual(response.data['status'], 'WAITING')
    
    def test_call_next_ticket(self):
        ticket = QueueTicket.objects.create(
            region=self.region,
            office=self.office,
            status='WAITING'
        )
        
        response = self.client.post(f'/api/counters/{self.counter.id}/call-next/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['ticket']['status'], 'CALLED')
    
    def test_start_service(self):
        ticket = QueueTicket.objects.create(
            region=self.region,
            office=self.office,
            counter=self.counter,
            status='CALLED'
        )
        
        response = self.client.post(f'/api/tickets/{ticket.id}/start-service/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'SERVING')
    
    def test_complete_service(self):
        ticket = QueueTicket.objects.create(
            region=self.region,
            office=self.office,
            counter=self.counter,
            status='SERVING'
        )
        
        response = self.client.post(f'/api/tickets/{ticket.id}/complete-service/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'SERVED')
    
    def test_supervisor_status(self):
        QueueTicket.objects.create(
            region=self.region,
            office=self.office,
            status='WAITING'
        )
        
        response = self.client.get(f'/api/supervisor/office/{self.office.id}/status/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('waiting_count', response.data)
        self.assertIn('active_counters', response.data)
