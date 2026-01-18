from django.contrib import admin
from .models import Ambulance, Checklist, ChecklistItem, RigCheck, RigCheckItem

admin.site.register(Ambulance)
admin.site.register(Checklist)
admin.site.register(ChecklistItem)
admin.site.register(RigCheck)
admin.site.register(RigCheckItem)
