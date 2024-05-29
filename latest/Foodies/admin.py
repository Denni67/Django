# Register your models here.
from django.contrib import admin # type: ignore
from.models import Product
from.models import CartItem,Restaurant,Category,UserProfile,Beverage,Sweet,Cake,Coupon,SubscriptionPlan,UserSubscription
admin.site.register(Product)
admin.site.register(CartItem)
admin.site.register(Restaurant)
admin.site.register(Category)
admin.site.register(UserProfile)
admin.site.register(Beverage)
admin.site.register(Sweet)
admin.site.register(Cake)
admin.site.register(Coupon)
admin.site.register(SubscriptionPlan)
admin.site.register(UserSubscription)