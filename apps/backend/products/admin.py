from django.contrib import admin

from products.models import ProductType, Product, ProductColor, ProductImage, Color


admin.site.register(Color)
admin.site.register(ProductType)
admin.site.register(Product)
admin.site.register(ProductColor)
admin.site.register(ProductImage)
