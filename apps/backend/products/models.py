from django.db import models


class Fabric(models.Model):
    name = models.CharField(max_length=100)


class Product(models.Model):
    name = models.TextField()
    description = models.TextField(blank=True)
    discount_percent = models.PositiveSmallIntegerField(default=0)
    price_uah = models.DecimalField(max_digits=10, decimal_places=2)
    price_usd = models.DecimalField(max_digits=10, decimal_places=2)
    is_bestseller = models.BooleanField(default=False)
    is_available = models.BooleanField(default=False) #For frontend. Button notify of availability

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(discount_percent__lte=100), name="product_discount_lte_100")
        ]


class ProductFabric(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    fabric = models.ForeignKey(Fabric, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True) #is this fabric currently available for this product

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["product", "fabric"], name="unique_product_fabric")
        ]
