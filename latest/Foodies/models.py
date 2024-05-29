from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone



class ProductManager(models.Manager):
    def expensive_items(self):
        """
        Retrieve food items with prices greater than a certain threshold.
        """
        return self.filter(price__gt=100)  # Example filter for expensive items, price greater than 10

    def search(self, query):
        """
        Search food items by name.
        """
        return self.filter(name__icontains=query)  # Case-insensitive search for food items containing the query in their name

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Restaurant(models.Model):
    restaurant_name = models.CharField(max_length=100,null=False)
    address = models.CharField(max_length=250)
    mobile_number = models.IntegerField(null=True)
    email = models.EmailField(default='')
    opening_hours = models.DecimalField(max_digits=9, decimal_places=2, null=True)
    logo = models.ImageField(upload_to='restaurant_logos/', default='logo')
    ratings = models.DecimalField(max_digits=3, decimal_places=1)

    def __str__(self):
        return self.restaurant_name
    


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='media/') 
    objects = ProductManager()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    
    def __str__(self):
        return self.name
  
    
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.product.name}'

class Order(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('OUT_FOR_DELIVERY', 'Out for Delivery'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="User")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total Amount")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING', verbose_name="Order Status")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        ordering = ['-created_at']

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.product.name} ({self.quantity})'


class Wishlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)

    def __str__(self):
        return f"Wishlist for {self.user.username}"

class Beverage(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='beverages/')
    

    def __str__(self):
        return self.name

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=False,default=1)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,null=False)
    quantity = models.PositiveIntegerField(default=1)
    date=models.DateTimeField(default=timezone.now)
    
    
    @property
    def total_price(self):
        return self.product.price * self.quantity
        

    def __str__(self):
        return f"{self.quantity} * {self.product.name}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth= models.DateField(null=True, blank=True)
    mobile_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(max_length=255, null=True, blank=True)
    
    def __str__(self):
        return self.user.username




class Sweet(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='sweets/')

    def __str__(self):
        return self.name
    

class Cake(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='cakes/')

    def __str__(self):
        return self.name
    
class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2)  # e.g., 20.00 for 20%
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.code

class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_days = models.IntegerField()  # duration of the plan in days

    def __str__(self):
        return self.name

class UserSubscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()

    def __str__(self):
        return f"{self.user.username} - {self.plan.name}"