from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from news.models import News
from news.search import NewsSearch
from cat.models import Cat
from subcat.models import SubCat
from main.models import Main
from trending.models import Trending

def search(request):
    """
    Search view for news articles
    """
    query = request.GET.get('q', '').strip()
    page = request.GET.get('page', 1)
    
    site = Main.objects.get(pk=2)
    cat = Cat.objects.all()
    subcat = SubCat.objects.all()
    trending = Trending.objects.all().order_by('-pk')[:3]
    lastnews = News.objects.filter(act=1).order_by('-pk')[:3]
    
    if query:
        # Use the search functionality
        results = NewsSearch.search(query, published_only=True)
        
        # Pagination
        paginator = Paginator(results, 10)  # 10 articles per page
        
        try:
            news_list = paginator.page(page)
        except PageNotAnInteger:
            news_list = paginator.page(1)
        except EmptyPage:
            news_list = paginator.page(paginator.num_pages)
        
        context = {
            'site': site,
            'cat': cat,
            'subcat': subcat,
            'trending': trending,
            'lastnews': lastnews,
            'news': news_list,
            'query': query,
            'total_results': results.count(),
        }
    else:
        context = {
            'site': site,
            'cat': cat,
            'subcat': subcat,
            'trending': trending,
            'lastnews': lastnews,
            'query': '',
            'total_results': 0,
        }
    
    return render(request, 'front/search_results.html', context)


def tag_search(request, tag):
    """
    Search news by specific tag
    """
    site = Main.objects.get(pk=2)
    cat = Cat.objects.all()
    subcat = SubCat.objects.all()
    trending = Trending.objects.all().order_by('-pk')[:3]
    lastnews = News.objects.filter(act=1).order_by('-pk')[:3]
    
    results = NewsSearch.search_by_tag(tag, published_only=True)
    
    page = request.GET.get('page', 1)
    paginator = Paginator(results, 10)
    
    try:
        news_list = paginator.page(page)
    except PageNotAnInteger:
        news_list = paginator.page(1)
    except EmptyPage:
        news_list = paginator.page(paginator.num_pages)
    
    context = {
        'site': site,
        'cat': cat,
        'subcat': subcat,
        'trending': trending,
        'lastnews': lastnews,
        'news': news_list,
        'tag': tag,
        'total_results': results.count(),
    }
    
    return render(request, 'front/tag_results.html', context)
