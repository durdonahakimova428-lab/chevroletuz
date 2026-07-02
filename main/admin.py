from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Banner, Category, Car, CarImage, News, Dealer, TestDriveRequest, Profile
)


class CarImageInline(admin.TabularInline):
    model = CarImage
    extra = 1
    fields = ("image", "order", "preview")
    readonly_fields = ("preview",)

    def preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:60px;border-radius:6px;" />', obj.image.url)
        return "-"
    preview.short_description = "Ko'rinish"


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ("title", "order", "is_active", "preview")
    list_editable = ("order", "is_active")
    readonly_fields = ("preview",)

    def preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:50px;border-radius:6px;" />', obj.image.url)
        return "-"
    preview.short_description = "Rasm"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "has_discount", "is_featured",
                     "is_new", "created_at", "preview")
    list_editable = ("has_discount", "is_featured", "is_new")
    list_filter = ("category", "is_featured", "is_new", "has_discount")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    inlines = [CarImageInline]
    readonly_fields = ("preview",)
    fieldsets = (
        ("Asosiy ma'lumot", {
            "fields": ("name", "slug", "category", "main_image", "preview")
        }),
        ("Narx", {
            "fields": ("price", "old_price", "has_discount")
        }),
        ("Tavsif", {
            "fields": ("short_description", "description")
        }),
        ("Texnik xususiyatlar", {
            "fields": ("engine", "transmission", "fuel_type", "seats")
        }),
        ("Holat", {
            "fields": ("is_featured", "is_new")
        }),
    )

    def preview(self, obj):
        if obj.main_image:
            return format_html('<img src="{}" style="height:70px;border-radius:6px;" />', obj.main_image.url)
        return "-"
    preview.short_description = "Ko'rinish"


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ("title", "is_published", "published_at", "preview")
    list_editable = ("is_published",)
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("preview",)

    def preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:60px;border-radius:6px;" />', obj.image.url)
        return "-"
    preview.short_description = "Rasm"


@admin.register(Dealer)
class DealerAdmin(admin.ModelAdmin):
    list_display = ("name", "city", "phone")


@admin.register(TestDriveRequest)
class TestDriveRequestAdmin(admin.ModelAdmin):
    list_display = ("full_name", "phone", "car", "created_at", "is_processed")
    list_editable = ("is_processed",)
    list_filter = ("is_processed",)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "phone")
