from django.contrib import admin
from .models import DetectionHistory


@admin.register(DetectionHistory)
class DetectionHistoryAdmin(admin.ModelAdmin):
    list_display = ['file_name', 'media_type', 'result', 'confidence', 'created_at']
    list_filter = ['media_type', 'result', 'created_at']
    search_fields = ['file_name']
    ordering = ['-created_at']
    readonly_fields = ['created_at']
