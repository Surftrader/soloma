from django.contrib import admin
from .models import Collection, Product, ProductImage, ProductVariant, Order, OrderItem, JournalArticle

# class ProductImageInline(admin.TabularInline):
#     model = ProductImage
#     extra = 1

# class ProductVariantInline(admin.TabularInline):
#     model = ProductVariant
#     extra = 1

# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     list_display = ('title', 'created_at')
#     prepopulated_fields = {'slug': ('title',)}
#     inlines = [ProductImageInline, ProductVariantInline]

# class OrderItemInline(admin.TabularInline):
#     model = OrderItem
#     extra = 0
#     readonly_fields = ('variant', 'quantity', 'price')

# @admin.register(Order)
# class OrderAdmin(admin.ModelAdmin):
#     list_display = ('id', 'first_name', 'last_name', 'email', 'total_amount', 'is_paid', 'created_at')
#     list_filter = ('is_paid', 'created_at')
#     readonly_fields = ('stripe_payment_intent_id', 'total_amount')
#     inlines = [OrderItemInline]

# @admin.register(JournalArticle)
# class JournalArticleAdmin(admin.ModelAdmin):
#     list_display = ('city', 'title', 'created_at')
#     prepopulated_fields = {'slug': ('title',)}
    
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_core_collection', 'created_at')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProductImageInline, ProductVariantInline]

@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'is_featured')
    prepopulated_fields = {'slug': ('title',)}

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('variant', 'quantity', 'price')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'total_amount', 'is_paid', 'created_at')
    list_filter = ('is_paid', 'created_at')
    readonly_fields = ('stripe_payment_intent_id', 'total_amount')
    inlines = [OrderItemInline]

@admin.register(JournalArticle)
class JournalArticleAdmin(admin.ModelAdmin):
    list_display = ('city', 'title', 'created_at')
    prepopulated_fields = {'slug': ('title',)}