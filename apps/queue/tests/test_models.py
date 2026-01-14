from django.test import TestCase
from apps.queue.models import Region, Office, Counter, Officer, QueueTicket
from apps.users.models import User


class RegionModelTestCase(TestCase):
    """Test Region model"""
    
    def test_region_creation(self):
        region = Region.objects.create(name='Dar es Salaam')
        self.assertEqual(str(region), 'Dar es Salaam')
        self.assertIsNotNone(region.created_at)


class OfficeModelTestCase(TestCase):
    """Test Office model"""
    
    def setUp(self):
        self.region = Region.objects.create(name='Dar es Salaam')
    
    def test_office_creation(self):
        office = Office.objects.create(name='Main Office', region=self.region)
        self.assertIn(self.region.name, str(office))
        self.assertEqual(office.region, self.region)


class CounterModelTestCase(TestCase):
    """Test Counter model"""
    
    def setUp(self):
        self.region = Region.objects.create(name='Dar es Salaam')
        self.office = Office.objects.create(name='Main Office', region=self.region)
    
    def test_counter_creation(self):
        counter = Counter.objects.create(name='Counter 1', office=self.office)
        self.assertEqual(counter.office, self.office)
        self.assertTrue(counter.is_active)


class QueueTicketModelTestCase(TestCase):
    """Test QueueTicket model"""
    
    def setUp(self):
        self.region = Region.objects.create(name='Dar es Salaam')
        self.office = Office.objects.create(name='Main Office', region=self.region)
    
    def test_ticket_creation(self):
        ticket = QueueTicket.objects.create(
            region=self.region,
            office=self.office,
            status='WAITING'
        )
        self.assertIsNotNone(ticket.ticket_number)
        self.assertEqual(ticket.status, 'WAITING')
        self.assertEqual(ticket.region, self.region)
        self.assertEqual(ticket.office, self.office)
    
    def test_ticket_number_generation(self):
        ticket1 = QueueTicket.objects.create(
            region=self.region,
            office=self.office
        )
        ticket2 = QueueTicket.objects.create(
            region=self.region,
            office=self.office
        )
        self.assertNotEqual(ticket1.ticket_number, ticket2.ticket_number)
        self.assertIn(str(self.office.id).zfill(3), ticket1.ticket_number)
