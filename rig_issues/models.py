from django.db import models
from django.contrib.auth.models import User
from rig_check.models import Ambulance

def issue_attachment_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/issue_attachments/issue_<id>/<filename>
    return f'issue_attachments/issue_{instance.issue.id}/{filename}'

class Issue(models.Model):
    STATUS_CHOICES = (
        ('Open', 'Open'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
    )

    ambulance = models.ForeignKey(Ambulance, on_delete=models.CASCADE, related_name='issues')
    reported_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='reported_issues')
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Open')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'#{self.id} - {self.title} for {self.ambulance.name}'

class IssueComment(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username} on Issue #{self.issue.id}'

class IssueAttachment(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to=issue_attachment_path)
    uploaded_by = models.ForeignKey(User, on_delete=models.PROTECT)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Attachment for Issue #{self.issue.id}'
