from django.contrib import admin
from .models import Issue, IssueComment, IssueAttachment

admin.site.register(Issue)
admin.site.register(IssueComment)
admin.site.register(IssueAttachment)
