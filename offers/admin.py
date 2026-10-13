from django.contrib import admin

from .models import Business, Category, Location, OfferImage


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'phone', 'is_active', 'is_verified', 'is_paid', 'created_at')
    list_filter = ('is_active', 'is_verified', 'is_paid', 'category', 'locations')
    search_fields = ('name', 'slug', 'address', 'phone', 'phone_alt', 'whatsapp')
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ('locations',)
    autocomplete_fields = ('category',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(OfferImage)
class OfferImageAdmin(admin.ModelAdmin):
    list_display = ('business', 'order', 'created_at')
    list_filter = ('business',)
    search_fields = ('business__name',)
    autocomplete_fields = ('business',)
    readonly_fields = ('created_at',)
