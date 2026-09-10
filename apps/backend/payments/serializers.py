from rest_framework import serializers

from payments.models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = (
            "id",
            "order",
            "currency",
            "amount",
            "provider",
            "status",
            "transaction_id",
            "paid_at",
            "created_at",
            "updated_at",
        )
        read_only_fields = fields
