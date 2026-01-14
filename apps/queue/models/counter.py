from django.db import models
from .office import Office


class Counter(models.Model):
    name = models.CharField(max_length=100)
    office = models.ForeignKey(Office, on_delete=models.CASCADE, related_name='counters')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.office.name}"

    class Meta:
        db_table = 'queue_counter'
        ordering = ['name']
