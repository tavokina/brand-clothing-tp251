from rest_framework import viewsets

from products.serializers import (ProductListSerializer,
                                  ProductDetailSerializer)
from products.models import Product




class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = None

    def get_serializer_class(self):
        if self.action == "list":
            return ProductListSerializer
        return ProductDetailSerializer
