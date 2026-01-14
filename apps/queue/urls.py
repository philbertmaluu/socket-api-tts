"""
URL configuration for queue app.
"""
from django.urls import path
from apps.queue.views import views

app_name = 'queue'

urlpatterns = [
    path('tickets/', views.ticket_create_view, name='ticket-create'),
    path('tickets/<int:ticket_id>/start-service/', views.ticket_start_service_view, name='ticket-start-service'),
    path('tickets/<int:ticket_id>/complete-service/', views.ticket_complete_service_view, name='ticket-complete-service'),
    path('counters/<int:counter_id>/call-next/', views.counter_call_next_view, name='counter-call-next'),
    path('supervisor/office/<int:office_id>/status/', views.supervisor_office_status_view, name='supervisor-office-status'),
]
