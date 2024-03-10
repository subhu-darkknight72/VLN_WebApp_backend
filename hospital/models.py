from django.db import models

# Create your models here.
class actionHistory(models.Model):
    # store two columns: action and observation as strings
    action = models.CharField(max_length=100)
    observation = models.CharField(max_length=500)

    class Meta:
        verbose_name_plural = "Action Histories"

    def __str__(self):
        return self.action
    