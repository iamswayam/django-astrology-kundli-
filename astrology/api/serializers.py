from rest_framework import serializers
from ..models import KundliDetails

class KundliDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = KundliDetails
        fields = '__all__'  # Serialize all fields in the model
        read_only_fields = ['id']  # Make 'id' field read-only