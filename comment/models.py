from __future__ import unicode_literals
from django.db import models

# Create your models here.

class Comment(models.Model):
    name = models.CharField(max_length=60, verbose_name="Name")
    email = models.EmailField(max_length=60, verbose_name="Email")
    cm = models.TextField(verbose_name="Comment")
    news_id = models.IntegerField()
    date = models.CharField(max_length=15)
    time = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    status = models.IntegerField(default=0, help_text="0=Pending, 1=Approved")
    
    class Meta:
        ordering = ['-id']
        indexes = [
            models.Index(fields=['news_id', 'status']),
            models.Index(fields=['-created_at']),
        ]
        verbose_name = "Comment"
        verbose_name_plural = "Comments"

    def __str__(self):
        return f"{self.name} - {self.cm[:50]}"
    
    def is_approved(self):
        """Check if comment is approved"""
        return self.status == 1
