import uuid
from io import BytesIO

from django.core.files.base import ContentFile
from django.db import models
from django.utils.text import slugify
from PIL import Image


class Location(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "location"
        verbose_name_plural = "Locations"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)

    class Meta:
        db_table = "category"
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Business(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=200)

    logo = models.ImageField(
        upload_to="business_logos/",
        blank=True,
        null=True
    )

    locations = models.ManyToManyField(
        Location,
        related_name="businesses",
        blank=True
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name="businesses",
        blank=True,
        null=True
    )

    address = models.TextField()
    map_url = models.URLField(blank=True, null=True)
    phone = models.CharField(max_length=15)
    phone_alt = models.CharField(max_length=15, blank=True, null=True)
    whatsapp = models.CharField(max_length=15, blank=True, null=True)
    website = models.URLField(blank=True, null=True)

    fb_url = models.URLField(blank=True, null=True)
    ig_url = models.URLField(blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "business"
        verbose_name_plural = "Businesses"
        ordering = ["name"]

    def __str__(self):
        return self.name


class OfferImage(models.Model):
    MAX_IMAGE_WIDTH = 1024
    WEBP_QUALITY = 85

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    business = models.ForeignKey(
        "Business",
        on_delete=models.CASCADE,
        related_name="offer_images"
    )

    image = models.ImageField(
        upload_to="offer_images/"
    )

    order = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "offer_image"
        ordering = ["order", "id"]
        verbose_name = "Offer Image"
        verbose_name_plural = "Offer Images"

    def __str__(self):
        return f"{self.business.name} - Image {self.id}"

    def save(self, *args, **kwargs):
        if self.image:
            self.compress_image()
        super().save(*args, **kwargs)

    def compress_image(self):
        image = Image.open(self.image)

        if image.mode not in ("RGB", "RGBA"):
            image = image.convert("RGB")

        if image.width > self.MAX_IMAGE_WIDTH:
            height = round((self.MAX_IMAGE_WIDTH / image.width) * image.height)
            image = image.resize((self.MAX_IMAGE_WIDTH, height), Image.Resampling.LANCZOS)

        output = BytesIO()
        image.save(output, format="WEBP", quality=self.WEBP_QUALITY, optimize=True)
        output.seek(0)

        self.image.save(
            f"{uuid.uuid4().hex}.webp",
            ContentFile(output.read()),
            save=False,
        )