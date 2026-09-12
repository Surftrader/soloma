from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    # Homepage
    path('', views.home_view, name='home'),
    
    # Catalog with text filters
    path('shop/', views.catalog_view, name='catalog'),
    
    # Product Detail Page (PDP)
    path('product/<slug:slug>/', views.product_detail_view, name='product_detail'),
    
    # Editorial Journal Index & Article Pages (Footer only)
    path('journal/', views.journal_index_view, name='journal_index'),
    path('journal/<slug:slug>/', views.journal_detail_view, name='journal_detail'),
    
    # Customer Care Tabs (Footer only)
    path('customer-care/', views.customer_care_view, name='customer_care'),
    
    # Action Endpoint for newsletter
    path('newsletter-signup/', views.newsletter_signup_view, name='newsletter_signup'),

    path('about/', views.about_view, name='about'),
    
    path('contact/', views.contact_view, name='contact'),

]
