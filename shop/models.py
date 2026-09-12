from django.db import models

class Collection(models.Model):
    """Story-led micro-collections (e.g., 'The Cashmere Story, woven in Mongolia')"""
    title = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} ({self.location})"


class Product(models.Model):
    """Base model for garments aligned with soloma.co structure"""
    collection = models.ForeignKey(Collection, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    tagline = models.CharField(max_length=255, help_text="One-line tagline under the title")
    description = models.TextField()
    fabric_care = models.TextField(help_text="Details & Fabric accordion content")
    fit_guide = models.TextField(help_text="Fit accordion content")
    is_core_collection = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class ProductImage(models.Model):
    """Side thumbnail strip: Front, Back, Fabric, Worn"""
    IMAGE_TYPES = [
        ('FRONT', 'Front View'),
        ('BACK', 'Back View'),
        ('FABRIC', 'Fabric Detail'),
        ('WORN', 'Worn / Editorial'),
    ]
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/')
    image_type = models.CharField(max_length=10, choices=IMAGE_TYPES, default='FRONT')

    def __str__(self):
        return f"{self.image_type} for {self.product.title}"


class ProductVariant(models.Model):
    """Inventory matrix: Grey, Ivory, Natural options x Sizes"""
    SIZE_CHOICES = [('XS', 'XS'), ('S', 'S'), ('M', 'M'), ('L', 'L'), ('XL', 'XL')]
    COLOR_CHOICES = [('GREY', 'Grey'), ('IVORY', 'Ivory'), ('NATURAL', 'Natural')]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    color = models.CharField(max_length=10, choices=COLOR_CHOICES)
    size = models.CharField(max_length=5, choices=SIZE_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2) # Medium weight 500 on UI
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.product.title} - {self.get_color_display()} - {self.size}"


class JournalArticle(models.Model):
    """Editorial travel and style vignettes for the Journal index page"""
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    city = models.CharField(max_length=100) # Lisbon, New York, Lviv
    venue = models.CharField(max_length=200) # Lviv Opera House, The Little Owl, etc.
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.city} — {self.title}"


class NewsletterSubscriber(models.Model):
    """Plain text underline field subscriber list"""
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
    


class Order(models.Model):
    """Customer order details for Stripe checkout"""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    
    # Shipping info (collected as plain text as requested)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    street_address = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=20)
    
    # Stripe integration tracking fields
    stripe_payment_intent_id = models.CharField(max_length=255, blank=True, null=True)
    is_paid = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Order #{self.id} - {self.email} - Paid: {self.is_paid}"


class OrderItem(models.Model):
    """Items inside a specific order"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    variant = models.ForeignKey(ProductVariant, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Fixed price at checkout

    def __str__(self):
        return f"{self.quantity}x {self.variant}"
