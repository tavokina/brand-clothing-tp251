from django.db import models


class Fabric(models.Model):
    name = models.CharField(max_length=100)

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


class ProductFabric(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="fabrics")
    fabric = models.ForeignKey(Fabric, on_delete=models.CASCADE, related_name="products")
    is_available = models.BooleanField(default=True) #is this fabric currently available for this product

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["product", "fabric"], name="unique_product_fabric")
        ]

    def __str__(self):
        return f"{self.product.name} - {self.fabric.name}"

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="products/")
    order = models.PositiveSmallIntegerField(default=0)


    class Meta:
        ordering = ["order"]
