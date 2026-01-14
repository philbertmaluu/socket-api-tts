from django.test import TestCase
from django.db import transaction
from apps.queue.models import Region, Office, Counter, QueueTicket
from apps.queue.services import (
    create_ticket,
    call_next_ticket,
    start_service,
    complete_service
)


class TicketServiceTestCase(TestCase):
    """Test ticket service functions"""
    
    def setUp(self):
        self.region = Region.objects.create(name='Dar es Salaam')
        self.office = Office.objects.create(name='Main Office', region=self.region)
        self.counter = Counter.objects.create(name='Counter 1', office=self.office)
    
    def test_create_ticket(self):
        ticket = create_ticket(self.region.id, self.office.id)
        self.assertEqual(ticket.status, 'WAITING')
        self.assertEqual(ticket.office_id, self.office.id)
        self.assertIsNotNone(ticket.ticket_number)
    
    def test_call_next_ticket_fifo(self):
        ticket1 = create_ticket(self.region.id, self.office.id)
        ticket2 = create_ticket(self.region.id, self.office.id)
        
        called_ticket = call_next_ticket(self.counter.id)
        self.assertEqual(called_ticket.id, ticket1.id)
        self.assertEqual(called_ticket.status, 'CALLED')
        self.assertEqual(called_ticket.counter_id, self.counter.id)
        self.assertIsNotNone(called_ticket.called_at)
    
    def test_call_next_ticket_no_waiting(self):
        result = call_next_ticket(self.counter.id)
        self.assertIsNone(result)
    
    def test_start_service(self):
        ticket = create_ticket(self.region.id, self.office.id)
        ticket = call_next_ticket(self.counter.id)
        
        ticket = start_service(ticket.id)
        self.assertEqual(ticket.status, 'SERVING')
    
    def test_complete_service(self):
        ticket = create_ticket(self.region.id, self.office.id)
        ticket = call_next_ticket(self.counter.id)
        ticket = start_service(ticket.id)
        
        ticket = complete_service(ticket.id)
        self.assertEqual(ticket.status, 'SERVED')
        self.assertIsNotNone(ticket.served_at)
    
    def test_status_flow(self):
        ticket = create_ticket(self.region.id, self.office.id)
        self.assertEqual(ticket.status, 'WAITING')
        
        ticket = call_next_ticket(self.counter.id)
        self.assertEqual(ticket.status, 'CALLED')
        
        ticket = start_service(ticket.id)
        self.assertEqual(ticket.status, 'SERVING')
        
        ticket = complete_service(ticket.id)
        self.assertEqual(ticket.status, 'SERVED')
