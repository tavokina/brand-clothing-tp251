from rest_framework import (viewsets,
                            filters)
from products.serializers import (ProductListSerializer,
                                  ProductDetailSerializer)
from products.models import Product




class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Basic ViewSet with ReadOnlyMode

    Has name search field and ordering via price (uah and usd),
    created_at (auto incremented time stamp in Product model. Depends on when was the product add to the db)
    is_bestseller (bool) and is_new_collection (bool).
    Basic ordering depends on when was the product add to the db (so the new products are shown first)

    """
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
