from django.db.models import Q
from .models import News

class NewsSearch:
    """
    Search functionality for news articles
    """
    
    @staticmethod
    def search(query, published_only=True):
        """
        Search news by title, content, tags
        
        Args:
            query: Search term
            published_only: Filter only published articles (act=1)
        
        Returns:
            QuerySet of matching news articles
        """
        if not query:
            return News.objects.none()
        
        # Search in multiple fields
        search_filter = (
            Q(name__icontains=query) |
            Q(short_txt__icontains=query) |
            Q(body_txt__icontains=query) |
            Q(tag__icontains=query) |
            Q(catname__icontains=query)
        )
        
        results = News.objects.filter(search_filter)
        
        if published_only:
            results = results.filter(act=1)
        
        return results.order_by('-id')
    
    @staticmethod
    def search_by_tag(tag, published_only=True):
        """
        Search news by specific tag
        """
        results = News.objects.filter(tag__icontains=tag)
        
        if published_only:
            results = results.filter(act=1)
        
        return results.order_by('-id')
    
    @staticmethod
    def get_related_articles(news_obj, limit=5):
        """
        Get related articles based on category and tags
        """
        # Get articles from same category
        related = News.objects.filter(
            catid=news_obj.catid,
            act=1
        ).exclude(id=news_obj.id)
        
        # If article has tags, prioritize articles with matching tags
        if news_obj.tag:
            tags = news_obj.get_tags_list()
            if tags:
                tag_query = Q()
                for tag in tags:
                    tag_query |= Q(tag__icontains=tag)
                
                related = related.filter(tag_query)
        
        return related.order_by('-show')[:limit]
