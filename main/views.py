from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Banner, Car, Category, News, Dealer, Profile
from .forms import RegisterForm, ProfileForm, TestDriveForm


def home(request):
    banners = Banner.objects.filter(is_active=True)
    featured_cars = Car.objects.filter(is_featured=True)[:6]
    discount_cars = Car.objects.filter(has_discount=True)[:6]
    news_list = News.objects.filter(is_published=True)[:4]
    categories = Category.objects.all()
    return render(request, "main/home.html", {
        "banners": banners,
        "featured_cars": featured_cars,
        "discount_cars": discount_cars,
        "news_list": news_list,
        "categories": categories,
    })


def car_list(request):
    cars = Car.objects.all()
    category_slug = request.GET.get("category")
    if category_slug:
        cars = cars.filter(category__slug=category_slug)
    categories = Category.objects.all()
    return render(request, "main/car_list.html", {
        "cars": cars,
        "categories": categories,
        "selected_category": category_slug,
    })


def car_detail(request, slug):
    car = get_object_or_404(Car, slug=slug)
    related_cars = Car.objects.exclude(id=car.id)[:3]
    form = TestDriveForm(initial={"car": car})
    if request.method == "POST":
        form = TestDriveForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "So'rovingiz qabul qilindi! Tez orada siz bilan bog'lanamiz.")
            return redirect("car_detail", slug=car.slug)
    return render(request, "main/car_detail.html", {
        "car": car,
        "related_cars": related_cars,
        "form": form,
    })


def news_list_view(request):
    news = News.objects.filter(is_published=True)
    return render(request, "main/news_list.html", {"news_list": news})


def news_detail(request, slug):
    news = get_object_or_404(News, slug=slug, is_published=True)
    return render(request, "main/news_detail.html", {"news": news})


def dealer_list(request):
    dealers = Dealer.objects.all()
    return render(request, "main/dealers.html", {"dealers": dealers})


def test_drive(request):
    form = TestDriveForm()
    if request.method == "POST":
        form = TestDriveForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "So'rovingiz qabul qilindi!")
            return redirect("home")
    return render(request, "main/test_drive.html", {"form": form})


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            Profile.objects.create(user=user)
            login(request, user)
            messages.success(request, "Ro'yxatdan muvaffaqiyatli o'tdingiz!")
            return redirect("home")
    else:
        form = RegisterForm()
    return render(request, "main/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Login yoki parol noto'g'ri!")
    return render(request, "main/login.html")


def logout_view(request):
    logout(request)
    return redirect("home")


@login_required
def profile_view(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profil yangilandi!")
            return redirect("profile")
    else:
        form = ProfileForm(instance=profile)
    return render(request, "main/profile.html", {"form": form, "profile": profile})
