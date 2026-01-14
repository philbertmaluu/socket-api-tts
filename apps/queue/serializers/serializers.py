from rest_framework import serializers
from apps.queue.models import QueueTicket, Counter


class QueueTicketSerializer(serializers.ModelSerializer):
    """Full ticket serialization"""
    region_name = serializers.CharField(source='region.name', read_only=True)
    office_name = serializers.CharField(source='office.name', read_only=True)
    counter_name = serializers.CharField(source='counter.name', read_only=True, allow_null=True)

    class Meta:
        model = QueueTicket
        fields = [
            'id', 'ticket_number', 'region_id', 'region_name',
            'office_id', 'office_name', 'counter_id', 'counter_name',
            'status', 'created_at', 'called_at', 'served_at'
        ]
        read_only_fields = ['ticket_number', 'created_at', 'called_at', 'served_at']


class QueueTicketCreateSerializer(serializers.Serializer):
    """For ticket creation (region_id, office_id)"""
    region_id = serializers.IntegerField()
    office_id = serializers.IntegerField()

    def validate(self, attrs):
        """Validate region and office exist and match"""
        from apps.queue.models import Region, Office
        
        try:
            office = Office.objects.get(id=attrs['office_id'])
            if office.region_id != attrs['region_id']:
                raise serializers.ValidationError(
                    "Office does not belong to the specified region"
                )
        except Office.DoesNotExist:
            raise serializers.ValidationError("Office not found")
        
        return attrs


class CounterCallNextSerializer(serializers.Serializer):
    """Response for call-next action"""
    ticket = QueueTicketSerializer(read_only=True)
    message = serializers.CharField(read_only=True)


class SupervisorDashboardSerializer(serializers.Serializer):
    """Office stats aggregation"""
    waiting_count = serializers.IntegerField()
    called_count = serializers.IntegerField()
    serving_count = serializers.IntegerField()
    served_count = serializers.IntegerField()
    active_counters = serializers.IntegerField()
    idle_counters = serializers.IntegerField()
    average_service_time_seconds = serializers.FloatField(allow_null=True)
    activity_feed = serializers.ListField()
