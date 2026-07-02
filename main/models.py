from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Banner(models.Model):
    """Bosh sahifadagi katta slayder (hero banner)."""
    title = models.CharField("Sarlavha", max_length=200)
    subtitle = models.CharField("Tagsarlavha", max_length=255, blank=True)
    image = models.ImageField("Rasm", upload_to="banners/")
    link = models.CharField("Havola (ixtiyoriy)", max_length=255, blank=True)
    order = models.PositiveIntegerField("Tartib raqami", default=0)
    is_active = models.BooleanField("Faol", default=True)

    class Meta:
        verbose_name = "Banner"
        verbose_name_plural = "Bannerlar"
        ordering = ["order", "-id"]

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField("Nomi", max_length=100)
    slug = models.SlugField("Slug", unique=True)

    class Meta:
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"

    def __str__(self):
        return self.name


class Car(models.Model):
    name = models.CharField("Model nomi", max_length=120)
    slug = models.SlugField("Slug", unique=True)
    category = models.ForeignKey(Category, verbose_name="Kategoriya",
                                  on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name="cars")
    main_image = models.ImageField("Asosiy rasm", upload_to="cars/")
    price = models.DecimalField("Narxi (so'm)", max_digits=14, decimal_places=2)
    old_price = models.DecimalField("Eski narx (chegirma uchun)", max_digits=14,
                                     decimal_places=2, null=True, blank=True)
    short_description = models.CharField("Qisqa tavsif", max_length=255, blank=True)
    description = models.TextField("To'liq tavsif", blank=True)

    engine = models.CharField("Dvigatel", max_length=100, blank=True)
    transmission = models.CharField("Transmissiya", max_length=100, blank=True)
    fuel_type = models.CharField("Yoqilg'i turi", max_length=100, blank=True)
    seats = models.PositiveSmallIntegerField("O'rindiqlar soni", default=5)

    is_featured = models.BooleanField("Bosh sahifada ko'rsatish", default=False)
    is_new = models.BooleanField("Yangi model", default=False)
    has_discount = models.BooleanField("Chegirmada", default=False)

    created_at = models.DateTimeField("Qo'shilgan sana", auto_now_add=True)

    class Meta:
        verbose_name = "Avtomobil"
        verbose_name_plural = "Avtomobillar"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("car_detail", kwargs={"slug": self.slug})

    @property
    def discount_percent(self):
        if self.old_price and self.old_price > self.price:
            return round((1 - self.price / self.old_price) * 100)
        return 0


class CarImage(models.Model):
    car = models.ForeignKey(Car, related_name="gallery", on_delete=models.CASCADE)
    image = models.ImageField("Rasm", upload_to="cars/gallery/")
    order = models.PositiveIntegerField("Tartib", default=0)

    class Meta:
        verbose_name = "Galereya rasmi"
        verbose_name_plural = "Galereya rasmlari"
        ordering = ["order"]

    def __str__(self):
        return f"{self.car.name} - {self.id}"


class News(models.Model):
    title = models.CharField("Sarlavha", max_length=200)
    slug = models.SlugField("Slug", unique=True)
    image = models.ImageField("Rasm", upload_to="news/")
    short_text = models.CharField("Qisqa matn", max_length=300, blank=True)
    content = models.TextField("To'liq matn", blank=True)
    published_at = models.DateTimeField("Sana", auto_now_add=True)
    is_published = models.BooleanField("Chop etilgan", default=True)

    class Meta:
        verbose_name = "Yangilik"
        verbose_name_plural = "Yangiliklar"
        ordering = ["-published_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("news_detail", kwargs={"slug": self.slug})


class Dealer(models.Model):
    name = models.CharField("Nomi", max_length=150)
    address = models.CharField("Manzil", max_length=255)
    phone = models.CharField("Telefon", max_length=50, blank=True)
    city = models.CharField("Shahar", max_length=100, blank=True)
    latitude = models.FloatField("Kenglik", null=True, blank=True)
    longitude = models.FloatField("Uzunlik", null=True, blank=True)

    class Meta:
        verbose_name = "Diler"
        verbose_name_plural = "Dilerlar"

    def __str__(self):
        return self.name


class TestDriveRequest(models.Model):
    full_name = models.CharField("F.I.SH.", max_length=150)
    phone = models.CharField("Telefon raqami", max_length=50)
    car = models.ForeignKey(Car, on_delete=models.SET_NULL, null=True, blank=True,
                             verbose_name="Avtomobil")
    message = models.TextField("Xabar", blank=True)
    created_at = models.DateTimeField("Yuborilgan sana", auto_now_add=True)
    is_processed = models.BooleanField("Ko'rib chiqilgan", default=False)

    class Meta:
        verbose_name = "So'rov"
        verbose_name_plural = "So'rovlar"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.full_name} - {self.phone}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    avatar = models.ImageField("Profil rasmi", upload_to="avatars/", blank=True, null=True)
    phone = models.CharField("Telefon raqami", max_length=50, blank=True)

    class Meta:
        verbose_name = "Profil"
        verbose_name_plural = "Profillar"

    def __str__(self):
        return self.user.username
