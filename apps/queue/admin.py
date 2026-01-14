from django.contrib import admin
from apps.queue.models import Region, Office, Counter, Officer, QueueTicket


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at', 'updated_at')
    list_filter = ('created_at',)
    search_fields = ('name',)


class CounterInline(admin.TabularInline):
    model = Counter
    extra = 1


@admin.register(Office)
class OfficeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'region', 'created_at', 'updated_at')
    list_filter = ('region', 'created_at')
    search_fields = ('name',)
    inlines = [CounterInline]


@admin.register(Counter)
class CounterAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'office', 'is_active', 'created_at', 'updated_at')
    list_filter = ('office', 'is_active', 'created_at')
    search_fields = ('name',)


@admin.register(Officer)
class OfficerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'counter', 'user', 'created_at', 'updated_at')
    list_filter = ('counter', 'created_at')
    search_fields = ('name',)


@admin.register(QueueTicket)
class QueueTicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'ticket_number', 'office', 'counter', 'status', 'created_at', 'called_at', 'served_at')
    list_filter = ('status', 'office', 'region', 'created_at')
    search_fields = ('ticket_number',)
    readonly_fields = ('created_at', 'called_at', 'served_at')
