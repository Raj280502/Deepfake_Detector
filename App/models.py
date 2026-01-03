from django.db import models
from django.utils import timezone

class DetectionHistory(models.Model):
    """Model to store detection history for user analytics"""
    
    MEDIA_TYPES = [
        ('video', 'Video'),
        ('image', 'Image'),
    ]
    
    RESULT_CHOICES = [
        ('Real', 'Real'),
        ('Fake', 'Fake'),
    ]
    
    file_name = models.CharField(max_length=255)
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPES, default='video')
    result = models.CharField(max_length=10, choices=RESULT_CHOICES)
    confidence = models.FloatField()
    frames_analyzed = models.IntegerField(null=True, blank=True)
    processing_time = models.FloatField(null=True, blank=True)  # in seconds
    created_at = models.DateTimeField(default=timezone.now)
    
    # Additional metadata
    file_size = models.BigIntegerField(null=True, blank=True)  # in bytes
    frame_predictions = models.JSONField(null=True, blank=True)  # Store individual frame predictions
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Detection History'
        verbose_name_plural = 'Detection Histories'
    
    def __str__(self):
        return f"{self.file_name} - {self.result} ({self.confidence:.1f}%)"
    
    @property
    def processing_time_display(self):
        """Return formatted processing time"""
        if self.processing_time:
            if self.processing_time < 1:
                return f"{self.processing_time * 1000:.0f}ms"
            return f"{self.processing_time:.1f}s"
        return "N/A"
    
    @property
    def file_size_display(self):
        """Return human-readable file size"""
        if not self.file_size:
            return "N/A"
        
        size = self.file_size
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} TB"
