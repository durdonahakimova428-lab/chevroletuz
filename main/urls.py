from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("avtomobillar/", views.car_list, name="car_list"),
    path("avtomobillar/<slug:slug>/", views.car_detail, name="car_detail"),
    path("yangiliklar/", views.news_list_view, name="news_list"),
    path("yangiliklar/<slug:slug>/", views.news_detail, name="news_detail"),
    path("dilerlar/", views.dealer_list, name="dealer_list"),
    path("test-drayv/", views.test_drive, name="test_drive"),
    path("royxatdan-otish/", views.register_view, name="register"),
    path("kirish/", views.login_view, name="login"),
    path("chiqish/", views.logout_view, name="logout"),
    path("profil/", views.profile_view, name="profile"),
]
