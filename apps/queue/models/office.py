from django.db import models
from .region import Region


class Office(models.Model):
    name = models.CharField(max_length=200)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='offices')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.region.name})"

    class Meta:
        db_table = 'queue_office'
        ordering = ['name']
