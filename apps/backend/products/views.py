from rest_framework import (viewsets,
                            filters)
from products.serializers import (ProductListSerializer,
                                  ProductDetailSerializer)
from products.models import Product




class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    filter_backends =  [filters.SearchFilter, filters.OrderingFilter]

    search_fields = ["name"]

    ordering_fields = [
        "price_uah",
        "price_usd",
        "created_at",
        "is_bestseller",
        "is_new_collection",
    ]
    ordering = ["-created_at"] #default sorting if the user didn't specify ordering

    def get_serializer_class(self):
        if self.action == "list":
            return ProductListSerializer
        return ProductDetailSerializer
