from django.db.models import Count, Q, Avg
from datetime import timedelta
from django.utils import timezone
from apps.queue.models import QueueTicket, Counter


def get_next_waiting_ticket(office_id):
    """Get oldest WAITING ticket for office (FIFO)"""
    return QueueTicket.objects.filter(
        office_id=office_id,
        status='WAITING'
    ).order_by('created_at').first()


def get_office_queue_stats(office_id):
    """Count tickets by status for an office"""
    return QueueTicket.objects.filter(
        office_id=office_id
    ).values('status').annotate(
        count=Count('id')
    )


def get_active_counters(office_id):
    """Get counters with active tickets (CALLED or SERVING)"""
    return Counter.objects.filter(
        office_id=office_id,
        is_active=True,
        tickets__status__in=['CALLED', 'SERVING']
    ).distinct()


def get_idle_counters(office_id):
    """Get counters without active tickets"""
    active_counter_ids = QueueTicket.objects.filter(
        office_id=office_id,
        status__in=['CALLED', 'SERVING'],
        counter__isnull=False
    ).values_list('counter_id', flat=True)
    
    return Counter.objects.filter(
        office_id=office_id,
        is_active=True
    ).exclude(id__in=active_counter_ids)


def get_ticket_by_id(ticket_id):
    """Get ticket with related objects"""
    return QueueTicket.objects.select_related(
        'region', 'office', 'counter'
    ).get(id=ticket_id)


def get_office_tickets(office_id, status=None):
    """Filter tickets by office and status"""
    queryset = QueueTicket.objects.filter(office_id=office_id)
    if status:
        queryset = queryset.filter(status=status)
    return queryset.order_by('created_at')


def _get_served_tickets(office_id):
    """Get served tickets with timing data"""
    return QueueTicket.objects.filter(
        office_id=office_id,
        status='SERVED',
        called_at__isnull=False,
        served_at__isnull=False
    )


def _calculate_service_times(served_tickets):
    """Calculate service times in seconds"""
    return [
        (ticket.served_at - ticket.called_at).total_seconds()
        for ticket in served_tickets
    ]


def calculate_average_service_time(office_id):
    """Calculate average service time from served tickets"""
    served_tickets = _get_served_tickets(office_id)
    if not served_tickets.exists():
        return None
    
    service_times = _calculate_service_times(served_tickets)
    if service_times:
        avg_seconds = sum(service_times) / len(service_times)
        return timedelta(seconds=avg_seconds)
    return None
