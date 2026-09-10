from django.contrib import admin

from products.models import (ProductType,
                             Product,
                             ProductColor,
                             ProductImage,
                             Color,
                             SizeGuide)


class SizeGuideInline(admin.StackedInline):
    model = SizeGuide
    extra = 0
    max_num = 1


admin.site.register(Color)
admin.site.register(Product)
admin.site.register(ProductColor)
admin.site.register(ProductImage)
admin.site.register(SizeGuide)

@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)
    inlines = [SizeGuideInline]

