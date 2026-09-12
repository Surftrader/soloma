from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Product, Collection, JournalArticle, NewsletterSubscriber

def home_view(request):
    """Homepage: Hero -> Curated Micro-collection -> Editorial pull-quote -> Centered Styling Carousel -> Need Help"""
    featured_collection = Collection.objects.filter(is_featured=True).first()
    featured_products = featured_collection.products.all()[:4] if featured_collection else []
    core_products = Product.objects.filter(is_core_collection=True)

    # Clean structured data for the centered "How to Style It" carousel
    styling_pairings = [
        {
            'title': 'Pastel Warmth',
            'city': 'Lisbon',
            'colors': [{'hex': '#F4F2EF', 'name': 'Shovk'}, {'hex': '#E0E0DB', 'name': 'Novvy Misyats'}],
            'mood': 'Dusk Setting',
            'desc': 'A gentle blend of natural cream and soft light grey tones, perfectly balancing comfort with old-money architecture.',
            'link': '/journal/lisbon/'
        },
        {
            'title': 'Bold Contrast',
            'city': 'New York',
            'colors': [{'hex': '#706867', 'name': 'Umbra'}, {'hex': '#403B3B', 'name': 'Deep Umbra'}],
            'mood': 'West Village Evening',
            'desc': 'Sharp, confident silhouettes meeting deep shadow tones. Designed for swift movement from coffee meetings to gallery openings.',
            'link': '/journal/new-york/'
        },
        {
            'title': 'Urban Serenity',
            'city': 'Lviv',
            'colors': [{'hex': '#F4F2EF', 'name': 'Shovk'}, {'hex': '#706867', 'name': 'Umbra'}],
            'mood': 'Coffeehouse Echoes',
            'desc': 'An homage to artisanal craft and historical texture. Soft beige tones paired with moody grey accents near the Opera House.',
            'link': '/journal/lviv/'
        }
    ]

    return render(request, 'shop/home.html', {
        'featured_collection': featured_collection,
        'featured_products': featured_products,
        'core_products': core_products,
        'styling_pairings': styling_pairings
    })


def catalog_view(request):
    """Catalog with clean text-row filtering and sorting (No boxes, no pills)"""
    products = Product.objects.all()
    
    # Simple extraction of text filters from request
    category_filter = request.GET.get('category', None)
    sort_by = request.GET.get('sort', 'newest')

    if category_filter:
        products = products.filter(collection__slug=category_filter)
        
    if sort_by == 'price_low':
        products = products.order_by('variants__price').distinct()
    elif sort_by == 'price_high':
        products = products.order_by('-variants__price').distinct()
    else:
        products = products.order_by('-created_at')

    return render(request, 'shop/catalog.html', {
        'products': products,
        'current_sort': sort_by,
        'current_category': category_filter
    })


def product_detail_view(request, slug):
    """Product Detail Page matching real soloma.co layout rules"""
    product = get_object_or_404(Product, slug=slug)
    
    # Structured measurements for the bottom-sheet Size & Fit Guide (pulled from real site data)
    size_chart = [
        {'size': 'XS', 'bust': '82-86 cm', 'waist': '62-66 cm', 'hips': '88-92 cm'},
        {'size': 'S', 'bust': '86-90 cm', 'waist': '66-70 cm', 'hips': '92-96 cm'},
        {'size': 'M', 'bust': '90-94 cm', 'waist': '70-74 cm', 'hips': '96-100 cm'},
        {'size': 'L', 'bust': '94-98 cm', 'waist': '74-78 cm', 'hips': '100-104 cm'},
        {'size': 'XL', 'bust': '98-102 cm', 'waist': '78-82 cm', 'hips': '104-108 cm'},
    ]
    
    # 2 Curated suggestions for "Wear It With" section (No redundant items)
    suggestions = Product.objects.exclude(id=product.id)[:2]

    return render(request, 'shop/product_detail.html', {
        'product': product,
        'size_chart': size_chart,
        'suggestions': suggestions
    })


def journal_index_view(request):
    """Journal index for editorial stories (Footer-only access)"""
    articles = JournalArticle.objects.all().order_by('-created_at')
    return render(request, 'shop/journal_index.html', {'articles': articles})


def journal_detail_view(request, slug):
    """Specific travel or styling vignette page"""
    article = get_object_or_404(JournalArticle, slug=slug)
    return render(request, 'shop/journal_detail.html', {'article': article})


def customer_care_view(request):
    """Unified Customer Care page split into 3 clean text accordion sections"""
    return render(request, 'shop/customer_care.html')


def newsletter_signup_view(request):
    """Handles minimalist newsletter subscription via inline underline inputs"""
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            NewsletterSubscriber.objects.get_or_create(email=email)
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'success'})
    return redirect('shop:home')

def about_view(request):
    return render(request, 'shop/about.html')

def contact_view(request):
    """Contact page with live form processing and embedded FAQ accordion summary"""
    return render(request, 'shop/contact.html')
