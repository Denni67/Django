

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, CartItem,Category,Order,UserProfile,Restaurant,Wishlist,Sweet,Cake
from .models import Coupon, SubscriptionPlan, UserSubscription
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.models import User
from .forms import SignUpForm, UserLoginForm
from .forms import UserForm, UserProfileForm
from django.contrib.auth import login as auth_login
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator,EmptyPage
from django.contrib import messages
from django.utils import timezone

def home(request):
    products= Product.objects.all() 
    return render(request, 'home.html', {'products': products})

def products(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})


def search(request):
    query = request.GET.get('query')
    if query:
        results = Product.objects.search(query)
    else:
        results = None
    context = {'results': results, 'query': query}
    return render(request, 'search.html', context)

def product_list(request):
    products = Product.objects.all()
    query = request.GET.get('query')
    sort_by = request.GET.get('sort_by')
    categories = request.GET.getlist('category')
    price_ranges = request.GET.getlist('price_range')
    ratings = request.GET.getlist('ratings')
    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))

    if categories:
        products = products.filter(category__id__in=categories)

    if price_ranges:
        price_filters = Q()
        for price_range in price_ranges:
            min_price, max_price = map(int, price_range.split('-'))
            price_filters |= Q(price__gte=min_price, price__lte=max_price)
        products = products.filter(price_filters)

    if ratings:
        products = products.filter(rating__gte=min(ratings))

    if sort_by:
        if sort_by == 'price_asc':
            products = products.order_by('price')
        elif sort_by == 'price_desc':
            products = products.order_by('-price')
        else:
            products = products.order_by('name')

    

    context = {
        'products': products,
        'categories': Category.objects.all(),
    }
    return render(request, 'product_list.html', context)
    

def detail_page(request, id):
    product= get_object_or_404(Product, pk=id)
    return render(request, 'detail.html', {'product': product})

def view_cart(request):
    cart_items=CartItem.objects.filter(user=request.user)
    total_price=sum(item.product.price*item.quantity for item in cart_items)
    return render(request,'cart.html',{'cart_items':cart_items,'total_price':total_price})

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(product=product, user=request.user)

    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    return redirect('view_cart')

def remove_from_cart(request,item_id):
    cart_item=CartItem.objects.get(id=item_id)
    cart_item.delete()
    return redirect('view_cart')
def user_signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            auth_login(request, user)  # Log in the user after signup
            return redirect('login')  # Redirect to the login page
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('list')  # Redirect to the homepage after successful login
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form, 'user': request.user})

def user_logout(request):
    logout(request)
    return redirect('list')  # Redirect to the homepage after logout


@login_required
def view_profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, instance=user_profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('view_profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=user_profile)

    return render(request, 'profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'user_profile': user_profile,
    })

    

def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        Review.objects.create(user=request.user, product=product, rating=rating, comment=comment)
        return redirect('product_detail', product_id=product.id)
    return render(request, 'add_review.html', {'product': product})    

def index(request):
    res=Restaurant.objects.all()
    return render(request,'index.html',{'res':res})
def add(request):
    return render(request,'add.html')

def addrec(request):
    x=request.POST['restaurant_name']
    y=request.POST['address']
    z=request.POST['mobile_number']
    a=request.POST['email']
    b=request.POST['opening_hours']
    c=request.POST['ratings']
    res=Restaurant(restaurant_name=x,address=y,mobile_number=z,email=a,opening_hours=b,ratings=c)
    res.save()
    return redirect("/")

def delete(request,id):
    res=Restaurant.objects.get(id=id)
    res.delete()
    return redirect("/")

def update(request,id):
    res=Restaurant.objects.get(id=id)
    return render(request,'update.html',{'res':res})

def uprec(request,id):
    x=request.POST['restaurant_name']
    y=request.POST['address']
    z=request.POST['mobile_number']
    a=request.POST['email']
    b=request.POST['opening_hours']
    c=request.POST['ratings']
    
    res=Restaurant.objects.get(id=id)
    res.restaurant_name=x
    res.address=y
    res.mobile_number=z
    res.email=a
    res.opening_hours=b
    res.ratings=c
    res.save()
    return redirect("/")



def view_wishlist(request):
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    return render(request, 'wishlist.html', {'wishlist': wishlist})

def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    wishlist.products.add(product)
    return redirect('list')

def remove_from_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    wishlist.products.remove(product)
    return redirect('view_wishlist')

def order_history(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'order_history.html', {'orders': orders})

def list_product(request,page=1):
    products=Product.objects.all()
    paginator =Paginator(products,5)
    try:

        products = paginator.page(page)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    
    return render (request,'product_list.html',{'products':products})



# def beverages(request):
#     beverages = Beverage.objects.all()
#     return render(request, 'beverages.html', {'beverages': beverages})


def sweets(request):
    sweets = Sweet.objects.all()
    return render(request, 'sweet.html', {'sweets': sweets})


def cakes(request):
    cakes = Cake.objects.all()
    return render(request, 'cakes.html', {'cakes': cakes})

# def add_to_cart_beverage(request, beverage_id):
#     beverage = get_object_or_404(Beverage, id=beverage_id)
#     cart_item, created = CartItem.objects.get_or_create(beverage=beverage, user=request.user)

#     if not created:
#         cart_item.quantity += 1
#         cart_item.save()
    
#     return redirect('view_cart')

# def add_to_wishlist_beverage(request, beverage_id):
#     beverage = get_object_or_404(Beverage, id=beverage_id)
#     wishlist, created = Wishlist.objects.get_or_create(user=request.user)
#     wishlist.products.add(beverage)
#     return redirect('list')


def subscription_plans(request):
    plans = SubscriptionPlan.objects.all()
    return render(request, 'subscription_plans.html', {'plans': plans})


@login_required
def subscribe(request):
    if request.method == 'POST':
        plan_id = request.POST['plan']
        plan = SubscriptionPlan.objects.get(id=plan_id)
        end_date = timezone.now() + timezone.timedelta(days=plan.duration_days)
        UserSubscription.objects.create(user=request.user, plan=plan, end_date=end_date)
        messages.success(request, f"You have subscribed to {plan.name}")
        return redirect('subscription_plans')
    plans = SubscriptionPlan.objects.all()
    return render(request, 'subscribe.html', {'plans': plans})

def apply_coupon(request):
    if request.method == 'POST':
        code = request.POST['code']
        try:
            coupon = Coupon.objects.get(code=code, active=True, valid_from__lte=timezone.now(), valid_to__gte=timezone.now())
            # Apply coupon logic (this is where you'd apply the discount to the cart or order)
            messages.success(request, f"Coupon {code} applied successfully!")
        except Coupon.DoesNotExist:
            messages.error(request, "Invalid or expired coupon code.")
        return redirect('view_cart')
    return render(request, 'apply_coupon.html')

def category_view(request, category_name):
    category = get_object_or_404(Category, name=category_name)
    products = Product.objects.filter(category=category)
    context = {
        'category': category,
        'products': products,
    }
    return render(request, 'category_view.html', context)