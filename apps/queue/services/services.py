from django.db import transaction
from django.utils import timezone
from apps.queue.models import QueueTicket, Counter
from apps.queue.selectors import (
    get_next_waiting_ticket,
    get_ticket_by_id,
    get_active_counters,
    get_idle_counters,
    get_office_queue_stats,
    calculate_average_service_time,
    get_office_tickets
)
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


channel_layer = get_channel_layer()


def broadcast_websocket_event(group_name, event_type, data):
    """Helper for WebSocket broadcasting"""
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            'type': 'queue_event',
            'event_type': event_type,
            'data': data
        }
    )


def broadcast_to_office(office_id, event_type, data):
    """Broadcast event to office group"""
    group_name = f'office_{office_id}'
    broadcast_websocket_event(group_name, event_type, data)


def broadcast_to_region(region_id, event_type, data):
    """Broadcast event to region group"""
    group_name = f'region_{region_id}'
    broadcast_websocket_event(group_name, event_type, data)


def broadcast_to_counter(counter_id, event_type, data):
    """Broadcast event to counter group"""
    group_name = f'counter_{counter_id}'
    broadcast_websocket_event(group_name, event_type, data)


def prepare_ticket_data(ticket):
    """Prepare ticket data for WebSocket events"""
    return {
        'ticket_id': ticket.id,
        'ticket_number': ticket.ticket_number,
        'region_id': ticket.region_id,
        'office_id': ticket.office_id,
        'counter_id': ticket.counter_id,
        'status': ticket.status,
        'timestamp': timezone.now().isoformat()
    }


@transaction.atomic
def create_ticket(region_id, office_id):
    """Create ticket, generate number, broadcast TICKET_CREATED"""
    ticket = QueueTicket.objects.create(
        region_id=region_id,
        office_id=office_id,
        status='WAITING'
    )
    
    data = prepare_ticket_data(ticket)
    broadcast_to_office(office_id, 'TICKET_CREATED', data)
    broadcast_to_region(region_id, 'TICKET_CREATED', data)
    
    return ticket


@transaction.atomic
def call_next_ticket(counter_id):
    """Get next WAITING ticket, assign to counter, update status to CALLED"""
    counter = Counter.objects.select_related('office').get(id=counter_id)
    ticket = get_next_waiting_ticket(counter.office_id)
    
    if not ticket:
        return None
    
    ticket.counter_id = counter_id
    ticket.status = 'CALLED'
    ticket.called_at = timezone.now()
    ticket.save()
    
    data = prepare_ticket_data(ticket)
    broadcast_to_office(counter.office_id, 'TICKET_CALLED', data)
    broadcast_to_region(counter.office.region_id, 'TICKET_CALLED', data)
    broadcast_to_counter(counter_id, 'TICKET_CALLED', data)
    
    return ticket


@transaction.atomic
def start_service(ticket_id):
    """Update status to SERVING, broadcast SERVICE_STARTED"""
    ticket = get_ticket_by_id(ticket_id)
    ticket.status = 'SERVING'
    ticket.save()
    
    data = prepare_ticket_data(ticket)
    broadcast_to_office(ticket.office_id, 'SERVICE_STARTED', data)
    
    return ticket


@transaction.atomic
def complete_service(ticket_id):
    """Update status to SERVED, set served_at, broadcast SERVICE_COMPLETED"""
    ticket = get_ticket_by_id(ticket_id)
    ticket.status = 'SERVED'
    ticket.served_at = timezone.now()
    ticket.save()
    
    data = prepare_ticket_data(ticket)
    broadcast_to_office(ticket.office_id, 'SERVICE_COMPLETED', data)
    
    return ticket


def _build_status_counts(stats_by_status):
    """Convert stats list to dictionary"""
    return {item['status']: item['count'] for item in stats_by_status}


def _build_activity_feed(recent_tickets):
    """Build activity feed from tickets"""
    return [
        {
            'ticket_number': t.ticket_number,
            'status': t.status,
            'counter_name': t.counter.name if t.counter else None,
            'timestamp': t.updated_at.isoformat()
        }
        for t in recent_tickets
    ]


def get_supervisor_dashboard_data(office_id):
    """Aggregate real-time stats for supervisor dashboard"""
    stats_by_status = get_office_queue_stats(office_id)
    status_counts = _build_status_counts(stats_by_status)
    
    waiting_count = status_counts.get('WAITING', 0)
    active_counters = get_active_counters(office_id).count()
    idle_counters = get_idle_counters(office_id).count()
    avg_service_time = calculate_average_service_time(office_id)
    recent_tickets = get_office_tickets(office_id)[:10]
    activity_feed = _build_activity_feed(recent_tickets)
    
    return {
        'waiting_count': waiting_count,
        'called_count': status_counts.get('CALLED', 0),
        'serving_count': status_counts.get('SERVING', 0),
        'served_count': status_counts.get('SERVED', 0),
        'active_counters': active_counters,
        'idle_counters': idle_counters,
        'average_service_time_seconds': avg_service_time.total_seconds() if avg_service_time else None,
        'activity_feed': activity_feed
    }
