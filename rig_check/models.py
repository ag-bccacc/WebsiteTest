from django.db import models
from django.contrib.auth.models import User

class Ambulance(models.Model):
    name = models.CharField(max_length=100, unique=True)
    is_in_service = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Checklist(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class ChecklistItem(models.Model):
    checklist = models.ForeignKey(Checklist, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=255)
    is_critical = models.BooleanField(default=False, help_text="A failed critical item will take the ambulance out of service.")

    def __str__(self):
        return f"{self.checklist.name} - {self.name}"

class RigCheck(models.Model):
    ambulance = models.ForeignKey(Ambulance, on_delete=models.PROTECT)
    checklist = models.ForeignKey(Checklist, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    timestamp = models.DateTimeField(auto_now_add=True)
    passed = models.BooleanField(default=True)

    def __str__(self):
        return f"Check for {self.ambulance.name} by {self.user.username} on {self.timestamp.strftime('%Y-%m-%d %H:%M')}"

class RigCheckItem(models.Model):
    STATUS_CHOICES = (
        ('Pass', 'Pass'),
        ('Fail', 'Fail'),
    )
    rig_check = models.ForeignKey(RigCheck, on_delete=models.CASCADE, related_name='items')
    checklist_item = models.ForeignKey(ChecklistItem, on_delete=models.PROTECT)
    status = models.CharField(max_length=4, choices=STATUS_CHOICES)
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.checklist_item.name}: {self.status}"

    def save(self, *args, **kwargs):
        if self.status == 'Fail' and self.checklist_item.is_critical:
            ambulance = self.rig_check.ambulance
            ambulance.is_in_service = False
            ambulance.save()
        super().save(*args, **kwargs)
