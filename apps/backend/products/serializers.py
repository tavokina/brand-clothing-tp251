from rest_framework import serializers
from decimal import Decimal, ROUND_HALF_UP
from products.models import Product, ProductImage, Color, ProductColor, SizeGuide


def _calc_discounted(price, discount_percent):
    multiplier = Decimal(100 - discount_percent) / Decimal(100)
    discounted = price * multiplier
    return str(discounted.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))

def _get_discounted_price_uah(obj):
    return _calc_discounted(obj.price_uah, obj.discount_percent)

def _get_discounted_price_usd(obj):
    return _calc_discounted(obj.price_usd, obj.discount_percent)


class SizeGuideSerializer(serializers.ModelSerializer):
    product_type = serializers.SlugRelatedField(many=False, slug_field="name", read_only=True)
    class Meta:
        model = SizeGuide
        fields = ("id", "product_type", "image", "description")

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ("id", "image", "order", "color")

class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ("name", "hex_code")

class ProductColorSerializer(serializers.ModelSerializer):
    colors = ColorSerializer(source="color", many=False)
    class Meta:
        model = ProductColor
        fields = ("colors", "is_available")

class ProductListSerializer(serializers.ModelSerializer):
    main_image = serializers.SerializerMethodField()
    discounted_price_uah = serializers.SerializerMethodField()
    discounted_price_usd = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ("id",
                  "name",
                  "main_image",
                  "price_uah",
                  "price_usd",
                  "is_available",
                  "discounted_price_uah",
                  "discounted_price_usd",
                  "is_bestseller",
                  "is_new_collection",
                  )

    def get_main_image(self, obj):
        first_image = obj.images.first() #we have ordering so it's gonna be an image with order = 0
        if first_image:
            return ProductImageSerializer(first_image, context=self.context).data
        return None

    def get_discounted_price_uah(self, obj):
        return _get_discounted_price_uah(obj)

    def get_discounted_price_usd(self, obj):
        return _get_discounted_price_usd(obj)


class ProductDetailSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    available_colors = ProductColorSerializer(source="colors", many=True)
    type = serializers.SlugRelatedField(many=False, slug_field="name", read_only=True)
    size_guide = serializers.SerializerMethodField()
    discounted_price_uah = serializers.SerializerMethodField()
    discounted_price_usd = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = ("id",
                  "name",
                  "type",
                  "description",
                  "price_uah",
                  "price_usd",
                  "discounted_price_uah",
                  "discounted_price_usd",
                  "is_bestseller",
                  "images",
                  "available_colors",
                  "is_available",
                  "size_guide")


    def get_size_guide(self, obj):
        size_guide = getattr(obj.type, "size_guide", None)
        if size_guide:
            return SizeGuideSerializer(size_guide, context=self.context).data
        return None

    def get_discounted_price_uah(self, obj):
        return _get_discounted_price_uah(obj)

    def get_discounted_price_usd(self, obj):
        return _get_discounted_price_usd(obj)
