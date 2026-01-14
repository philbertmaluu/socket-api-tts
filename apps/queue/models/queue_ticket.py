from django.db import models
from django.utils import timezone
from .region import Region
from .office import Office
from .counter import Counter


class QueueTicket(models.Model):
    STATUS_CHOICES = [
        ('WAITING', 'Waiting'),
        ('CALLED', 'Called'),
        ('SERVING', 'Serving'),
        ('SERVED', 'Served'),
    ]

    ticket_number = models.CharField(max_length=50, unique=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='tickets')
    office = models.ForeignKey(Office, on_delete=models.CASCADE, related_name='tickets')
    counter = models.ForeignKey(Counter, on_delete=models.SET_NULL, null=True, blank=True, related_name='tickets')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='WAITING')
    created_at = models.DateTimeField(auto_now_add=True)
    called_at = models.DateTimeField(null=True, blank=True)
    served_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.ticket_number} - {self.status}"

    def _get_last_ticket_number(self):
        """Get last ticket number for today"""
        from datetime import datetime
        return QueueTicket.objects.filter(
            office=self.office,
            created_at__date=datetime.now().date()
        ).order_by('-id').first()
    
    def _get_next_sequence_number(self, last_ticket):
        """Get next sequence number"""
        if last_ticket:
            last_num = int(last_ticket.ticket_number.split('-')[-1])
            return str(last_num + 1).zfill(4)
        return '0001'
    
    def generate_ticket_number(self):
        """Generate unique ticket number in format: OFFICE-YYYYMMDD-XXXX"""
        from datetime import datetime
        office_code = str(self.office.id).zfill(3)
        date_str = datetime.now().strftime('%Y%m%d')
        last_ticket = self._get_last_ticket_number()
        new_num = self._get_next_sequence_number(last_ticket)
        return f"{office_code}-{date_str}-{new_num}"

    def save(self, *args, **kwargs):
        if not self.ticket_number:
            self.ticket_number = self.generate_ticket_number()
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'queue_ticket'
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['office', 'status', 'created_at']),
            models.Index(fields=['status']),
        ]
