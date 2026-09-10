from django.db import models


class Color(models.Model):
    name = models.CharField(max_length=100)
    hex_code = models.CharField(max_length=7, blank=True) # for example "#FF0000" for frontend


    def __str__(self):
        return self.name

class ProductType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.TextField()
    type = models.ForeignKey(ProductType, on_delete=models.PROTECT, related_name="products")
    description = models.TextField(blank=True)
    fabric_composition = models.CharField(max_length=255, blank=True) # "100% cotton"
    discount_percent = models.PositiveSmallIntegerField(default=0)
    price_uah = models.DecimalField(max_digits=10, decimal_places=2)
    price_usd = models.DecimalField(max_digits=10, decimal_places=2)
    is_bestseller = models.BooleanField(default=False)
    is_available = models.BooleanField(default=False) #For frontend. Button notify of availability

    class Meta:
        constraints = [
            models.CheckConstraint(condition=models.Q(discount_percent__lte=100), name="product_discount_lte_100")
        ]

    def __str__(self):
        return f"{self.type} - {self.name}"


class ProductColor(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="colors")
    color = models.ForeignKey(Color, on_delete=models.CASCADE, related_name="products")
    is_available = models.BooleanField(default=True) # is this color available for this product right now


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    color = models.ForeignKey(Color, on_delete=models.CASCADE, related_name="images", null=True, blank=True) # for future frontend functionally. Clicking on Color in Detail view will change the picture with the same color. If color=None need fallback logic for frontend
    image = models.ImageField(upload_to="products/") #will develop later using S3 AWS bucket
    order = models.PositiveSmallIntegerField(default=0) #for frontend. Order = 0 decides which photo is main one


    class Meta:
        ordering = ["order"]
        constraints = [
            models.UniqueConstraint(
                fields=["product"],
                condition=models.Q(order=0),
                name="unique_main_image_per_product"
            )
        ]
