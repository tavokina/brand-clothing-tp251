from django.db import models


class Fabric(models.Model):
    """
    DEPRECATED: Temporary placeholder for backward compatibility with orders/models.py,
    pending other dev update to OrderItem.fabric. Remove after the orders fix.

    Not used anywhere in the products app itself — fabric composition on Product
    is stored as plain text (see Product.fabric_composition_ua/_eng below).
    This class only exists so that `from products.models import Fabric` in
    orders/models.py doesn't raise an ImportError while that app is being updated.
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Color(models.Model):
    """
    Reference list of colors available across all products.

    Colors are stored in English only (no _ua/_eng split) — color names
    are treated as universal labels shown the same way regardless of site language.
    """
    name = models.CharField(max_length=100)
    hex_code = models.CharField(max_length=7, blank=True)  # for example "#FF0000" for frontend

    def __str__(self):
        return self.name


class ProductType(models.Model):
    """
    Category/type of product (e.g. Dress, Skirt, Set, Shorts).

    Used both to group products and to attach a shared SizeGuide,
    since products of the same type generally share the same size chart.
    """
    name_ua = models.CharField(max_length=100)
    name_eng = models.CharField(max_length=100)

    def __str__(self):
        return self.name_ua


class Product(models.Model):
    """
    A single product listing.

    Bilingual fields (description, fabric_composition) are split into
    explicit _ua/_eng pairs rather than using a translation library,
    since the site only supports two fixed languages. `name` itself
    is not currently translated — same value is shown in both languages.

    Price is stored in both currencies directly (price_uah, price_usd)
    rather than converted at read time, so exchange rate fluctuations
    don't silently change displayed prices.
    """
    name = models.CharField(max_length=255)
    type = models.ForeignKey(ProductType, on_delete=models.PROTECT, related_name="products")
    description_ua = models.TextField(blank=True)
    description_eng = models.TextField(blank=True)
    fabric_composition_ua = models.CharField(max_length=255, blank=True)  # "100% бавовна"
    fabric_composition_eng = models.CharField(max_length=255, blank=True)  # "100% cotton"
    discount_percent = models.PositiveSmallIntegerField(default=0)
    price_uah = models.DecimalField(max_digits=10, decimal_places=2)
    price_usd = models.DecimalField(max_digits=10, decimal_places=2)
    is_bestseller = models.BooleanField(default=False)
    is_new_collection = models.BooleanField(default=False)  # For frontend. New collection flag for frontend logic
    is_available = models.BooleanField(default=False)  # For frontend. Button notify of availability
    created_at = models.DateTimeField(auto_now_add=True)  # for publication time sorting

    class Meta:
        constraints = [
            models.CheckConstraint(condition=models.Q(discount_percent__lte=100), name="product_discount_lte_100")
        ]

    def __str__(self):
        return f"{self.type} - {self.name}"


class SizeGuide(models.Model):
    """
    Size chart attached to a ProductType (one size guide per type,
    shared by all products of that type — not per individual product).

    image holds an optional visual size chart; description_ua/_eng hold
    optional accompanying text (e.g. measuring instructions).
    """
    product_type = models.OneToOneField(
        ProductType, on_delete=models.CASCADE, related_name="size_guide"
    )
    image = models.ImageField(upload_to="size_guides/", blank=True, null=True)
    description_ua = models.TextField(blank=True)  # Text description for size guide if needed
    description_eng = models.TextField(blank=True)


class ProductColor(models.Model):
    """
    Through model linking a Product to a Color it's offered in.

    is_available tracks whether this specific color is currently in stock
    for this specific product — independent of the product's own
    is_available flag (a product can be "available" overall while
    one of its colors is temporarily out of stock).
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="colors")
    color = models.ForeignKey(Color, on_delete=models.CASCADE, related_name="products")
    is_available = models.BooleanField(default=True)  # is this color available for this product right now


class ProductImage(models.Model):
    """
    A single image belonging to a product.

    color links the image to a specific color variant, so the frontend
    can swap the displayed photo when the user clicks a color swatch.
    color=None means the image is generic (not tied to any specific
    color) — the frontend needs fallback logic for this case.

    order determines display order within the gallery; order=0 is
    reserved for the product's main/cover image (enforced by the
    unique_main_image_per_product constraint below, which guarantees
    at most one order=0 image per product).
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    color = models.ForeignKey(Color, on_delete=models.CASCADE, related_name="images", null=True, blank=True)
    image = models.ImageField(upload_to="products/")  # will develop later using S3 AWS bucket
    order = models.PositiveSmallIntegerField(default=0)  # for frontend. order = 0 decides which photo is main one

    class Meta:
        ordering = ["order"]
        constraints = [
            models.UniqueConstraint(
                fields=["product"],
                condition=models.Q(order=0),
                name="unique_main_image_per_product"
            )
        ]
