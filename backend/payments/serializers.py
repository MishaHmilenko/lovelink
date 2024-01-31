import stripe
from rest_framework import serializers


class ProductsSerializer(serializers.Serializer):

    def to_representation(self, instance):
        price_object = stripe.Price.retrieve(instance['default_price'])

        instance['price'] = price_object['unit_amount'] / 100
        instance['currency'] = price_object['currency']

        return {
            'name': instance['name'],
            'price': instance['price'],
            'currency': instance['currency']
        }


class CreateCheckOutSessionSerializer(serializers.Serializer):
    prod_id = serializers.CharField()

