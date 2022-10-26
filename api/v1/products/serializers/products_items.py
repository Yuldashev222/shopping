from datetime import date
from rest_framework import serializers

from api.v1.products.models import ProductItem


class ProductItemSerializer(serializers.ModelSerializer):
    creator = serializers.HiddenField(default=serializers.CurrentUserDefault())
    category_id = serializers.IntegerField()
    date_created = serializers.DateTimeField(read_only=True, write_only=False)
    date_updated = serializers.DateTimeField(read_only=True, write_only=False)
    is_active = serializers.BooleanField(default=True)

    class Meta:
        model = ProductItem
        fields = '__all__'

    def validate(self, attrs):
        errors = dict()

        #  available_to_date and available_from_date validations ---------------
        today_date = date.today()
        available_from_date = attrs.get('available_from_date')
        available_to_date = attrs.get('available_to_date')
        if available_from_date and available_to_date:
            if available_from_date < today_date:
                errors['available_from_date'] = ['the available date must not be less than today\'s date']
            if available_from_date >= available_from_date:
                errors['available_to_date'] = ['the available from data must be less than the to date']

        elif available_from_date and available_from_date < today_date:
            errors['available_from_date'] = ['the available date must not be less than today\'s date']

        elif available_from_date:
            if available_from_date <= today_date:
                errors['available_to_date'] = ['the available to data must be to day date']
            else:
                attrs['available_from_date'] = today_date
        #  ------------------------------------------------

        if errors:
            raise serializers.ValidationError(errors)

        return attrs
