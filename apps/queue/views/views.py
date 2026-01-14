from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from apps.queue.models import Counter, QueueTicket
from apps.queue.services import (
    create_ticket,
    call_next_ticket,
    start_service,
    complete_service,
    get_supervisor_dashboard_data
)
from apps.queue.serializers import (
    QueueTicketSerializer,
    QueueTicketCreateSerializer,
    CounterCallNextSerializer,
    SupervisorDashboardSerializer
)


@api_view(['POST'])
def ticket_create_view(request):
    """Create ticket from kiosk (POST /api/tickets/)"""
    serializer = QueueTicketCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    ticket = create_ticket(
        region_id=serializer.validated_data['region_id'],
        office_id=serializer.validated_data['office_id']
    )
    
    return Response(
        QueueTicketSerializer(ticket).data,
        status=status.HTTP_201_CREATED
    )


@api_view(['POST'])
def counter_call_next_view(request, counter_id):
    """Officer calls next ticket (POST /api/counters/{id}/call-next/)"""
    counter = get_object_or_404(Counter, id=counter_id)
    
    if not counter.is_active:
        return Response(
            {'error': 'Counter is not active'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    ticket = call_next_ticket(counter_id)
    
    if not ticket:
        return Response(
            {'message': 'No waiting tickets available'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    return Response({
        'ticket': QueueTicketSerializer(ticket).data,
        'message': f'Ticket {ticket.ticket_number} called to counter {counter.name}'
    })


@api_view(['POST'])
def ticket_start_service_view(request, ticket_id):
    """Start serving ticket (POST /api/tickets/{id}/start-service/)"""
    ticket = get_object_or_404(QueueTicket, id=ticket_id)
    
    if ticket.status != 'CALLED':
        return Response(
            {'error': f'Ticket must be CALLED status, current status: {ticket.status}'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    ticket = start_service(ticket_id)
    return Response(QueueTicketSerializer(ticket).data)


@api_view(['POST'])
def ticket_complete_service_view(request, ticket_id):
    """Complete service (POST /api/tickets/{id}/complete-service/)"""
    ticket = get_object_or_404(QueueTicket, id=ticket_id)
    
    if ticket.status != 'SERVING':
        return Response(
            {'error': f'Ticket must be SERVING status, current status: {ticket.status}'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    ticket = complete_service(ticket_id)
    return Response(QueueTicketSerializer(ticket).data)


@api_view(['GET'])
def supervisor_office_status_view(request, office_id):
    """Get office stats (GET /api/supervisor/office/{office_id}/status/)"""
    dashboard_data = get_supervisor_dashboard_data(office_id)
    serializer = SupervisorDashboardSerializer(dashboard_data)
    return Response(serializer.data)
