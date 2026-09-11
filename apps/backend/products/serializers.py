from rest_framework import serializers
from decimal import Decimal, ROUND_HALF_UP
from products.models import (Product,
                             ProductImage,
                             Color,
                             ProductColor,
                             SizeGuide)


class LanguageMixin:
    def _lang(self):
        request = self.context.get("request")
        lang = request.GET.get("lang", "ua") if request else "ua"
        return "eng" if lang == "en" else "ua"


class CurrencyMixin:
    def _currency(self):
        request = self.context.get("request")
        currency = request.GET.get("currency", "uah") if request else "uah"
        return "usd" if currency == "usd" else "uah"

def _calc_discounted(price, discount_percent):
    multiplier = Decimal(100 - discount_percent) / Decimal(100)
    discounted = price * multiplier
    return str(discounted.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def _get_discounted_price(obj, currency):
    if not obj.discount_percent:
        return None
    price = obj.price_usd if currency == "usd" else obj.price_uah
    return _calc_discounted(price, obj.discount_percent)



class SizeGuideSerializer(LanguageMixin, serializers.ModelSerializer):
    description = serializers.SerializerMethodField()

    class Meta:
        model = SizeGuide
        fields = ("id", "image", "description")

    def get_description(self, obj):
        return obj.description_eng if self._lang() == "eng" else obj.description_ua


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

class ProductListSerializer(LanguageMixin, CurrencyMixin, serializers.ModelSerializer):
    main_image = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    discounted_price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ("id",
                  "name",
                  "main_image",
                  "price",
                  "discounted_price",
                  "is_available",
                  "is_bestseller",
                  "is_new_collection",
                  )

    def get_price(self, obj):
        price = obj.price_usd if self._currency() == "usd" else obj.price_uah
        return str(price)

    def get_discounted_price(self, obj):
        return _get_discounted_price(obj, self._currency())


    def get_main_image(self, obj):
        first_image = obj.images.first() #we have ordering so it's gonna be an image with order = 0
        if first_image:
            return ProductImageSerializer(first_image, context=self.context).data
        return None


class ProductDetailSerializer(LanguageMixin, CurrencyMixin, serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    available_colors = ProductColorSerializer(source="colors", many=True)
    type = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    fabric_composition = serializers.SerializerMethodField()
    size_guide = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    discounted_price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ("id", "name", "type", "description", "fabric_composition",
                  "price", "discounted_price",
                  "is_bestseller", "images", "available_colors", "is_available", "size_guide")

    def get_price(self, obj):
        price = obj.price_usd if self._currency() == "usd" else obj.price_uah

        return str(price)

    def get_type(self, obj):
        return obj.type.name_eng if self._lang() == "eng" else obj.type.name_ua

    def get_description(self, obj):
        return obj.description_eng if self._lang() == "eng" else obj.description_ua

    def get_fabric_composition(self, obj):
        return obj.fabric_composition_eng if self._lang() == "eng" else obj.fabric_composition_ua

    def get_size_guide(self, obj):
        size_guide = getattr(obj.type, "size_guide", None)
        if size_guide:
            return SizeGuideSerializer(size_guide, context=self.context).data
        return None

    def get_discounted_price(self, obj):
        return _get_discounted_price(obj, self._currency())
