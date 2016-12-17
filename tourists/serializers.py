from rest_framework import serializers

from data.fields import DepartmentField

from .models import Tourist, TouristCard


class TouristSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tourist
        fields = ('id', 'first_name', 'middle_name', 'last_name', 'email', 'date_joined',)
        read_only_fields = ('date_joined',)


class TouristCardSerializer(serializers.ModelSerializer):

    tourist = TouristSerializer()
    current_department = DepartmentField()
    card_id = serializers.SerializerMethodField()

    class Meta:
        model = TouristCard
        fields = ('card_id', 'is_active', 'current_department', 'created', 'tourist',)
        read_only = ('created', 'card_id',)

    def get_card_id(self, obj):
        return obj.card_id.hex

    def update(self, instance, validated_data):
        """
        Update nested tourist info over tourist card manually.
        """
        tourist = TouristSerializer(instance=instance.tourist, data=validated_data.get('tourist'))
        if tourist.is_valid():
            tourist.save()
        return instance

    def create(self, validated_data):
        """
        Create manually tourist info from tourist card data.
        """
        tourist_data = validated_data.pop('tourist')
        tourist = Tourist.objects.create(**tourist_data)
        tourist_card = TouristCard.objects.create(tourist=tourist, **validated_data)
        return tourist_card
