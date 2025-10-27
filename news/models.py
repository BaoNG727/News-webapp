from __future__ import unicode_literals
from django.db import models
from django.utils.text import slugify

# Create your models here.

class News(models.Model):
    name = models.CharField(max_length=200, verbose_name="Title")
    slug = models.SlugField(max_length=250, unique=True, blank=True, help_text="Auto-generated from title")
    short_txt = models.TextField(verbose_name="Short Description")
    body_txt = models.TextField(verbose_name="Content")
    date = models.CharField(max_length=12)
    time = models.CharField(max_length=12, default="00:00")
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    picname = models.TextField()
    picurl = models.TextField(default="-")
    writer = models.CharField(max_length=100)
    catname = models.CharField(max_length=100, default="-")
    catid = models.IntegerField(default=0)
    ocatid = models.IntegerField(default=0)  # ocatid means original cat id.for count news
    show = models.IntegerField(default=0)   # View count
    tag = models.TextField(default="", help_text="Separate tags with commas")
    act = models.IntegerField(default=0)  # For Publish News (0=draft, 1=published)
    rand = models.IntegerField(default=0)  # For Random Number of the News
    
    # SEO Fields
    meta_description = models.CharField(max_length=160, blank=True, help_text="SEO meta description (max 160 chars)")
    meta_keywords = models.CharField(max_length=255, blank=True, help_text="SEO keywords, separated by commas")

    class Meta:
        ordering = ['-id']
        indexes = [
            models.Index(fields=['-id', 'act']),
            models.Index(fields=['slug']),
            models.Index(fields=['catid', 'act']),
            models.Index(fields=['-show']),
        ]
        verbose_name = "News Article"
        verbose_name_plural = "News Articles"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while News.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        
        if not self.meta_description and self.short_txt:
            self.meta_description = self.short_txt[:160]
        
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.name
    
    def get_tags_list(self):
        """Return tags as a list"""
        return [tag.strip() for tag in self.tag.split(',') if tag.strip()]