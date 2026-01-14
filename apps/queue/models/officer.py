from django.db import models
from apps.users.models import User
from .counter import Counter


class Officer(models.Model):
    name = models.CharField(max_length=200)
    counter = models.ForeignKey(Counter, on_delete=models.SET_NULL, null=True, blank=True, related_name='officers')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='officer_profile')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.counter.name if self.counter else 'No Counter'}"

    class Meta:
        db_table = 'queue_officer'
        ordering = ['name']
