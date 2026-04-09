from django.db import models
from variables.models import Project

class CostRecord(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, default=None)
    service = models.CharField(max_length=100)
    amount = models.FloatField(null=True, blank=True, default=None)
    region = models.CharField(max_length=50)
    dateTime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s $%s' % (self.service, self.amount)
