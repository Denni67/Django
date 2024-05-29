from django.urls import path
from . import views
from django.conf.urls.static import static
from .views import subscription_plans,subscribe, apply_coupon,category_view

urlpatterns=[path('', views.home, name="list"),
             path('products', views.products, name="productpage"),
             path('<int:id>/', views.detail_page, name="detail"),
             path('search', views.search, name="search"),
             path('login/', views.user_login, name="login"),
             path('signup/', views.user_signup, name="signup"),
             path('logout/', views.user_logout, name="logout"),
             path('pro', views.product_list, name="product_list"),
             path('cart/',views.view_cart,name='view_cart'),
             path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
             path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
             path('profile/', views.view_profile, name='view_profile'),
             path('product/<int:product_id>/review/', views.add_review, name='add_review'),
             path('ap',views.index,name="index"),
             path('add/',views.add,name="add"),
             path('addrec/',views.addrec,name="addrec"),
             path('delete/<int:id>/', views.delete, name="delete"),
             path('update/<int:id>/', views.update, name="update"),
             path('update/uprec/<int:id>/', views.uprec, name="uprec"),
             path('wishlist/', views.view_wishlist, name='view_wishlist'),  # URL for wishlist
             path('add_to_wishlist/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),  # URL for adding to wishlist
             path('remove_from_wishlist/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'), # URL for removing from wishlist,
             path('order_history/', views.order_history, name='order_history'),
             path('products/<int:page>/', views.list_product, name='list_product'),
             path('category/<str:category_name>/', views.category_view, name='category_view'),
            #  path('add_to_cart_beverage/<int:beverage_id>/', views.add_to_cart_beverage, name='add_to_cart_beverage')    
            path('subscriptions/', subscription_plans, name='subscription_plans'),
            path('subscribe/', subscribe, name='subscribe'),
            path('apply_coupon/', apply_coupon, name='apply_coupon'),
            
]



             

               
