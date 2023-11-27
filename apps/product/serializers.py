from django.db.models import Avg
from  rest_framework import  serializers

from apps.product.models import Product


class ProductSerializer(serializers.ModelSerializer):
    owner_email = serializers.ReadOnlyField(
        source='owner.email'
    )
    owner = serializers.ReadOnlyField(source='owner.id')

    class Meta:
        model = Product
        fields = "__all__"

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['rating'] = instance.ratings.aggregate(Avg('rating'))
        rating = repr['rating']
        rating['rating__count'] = instance.ratings.count()
        return repr