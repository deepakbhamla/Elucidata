from rest_framework import serializers
from .models import File
class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = "__all__"


# class YourSerializer(serializers.Serializer):
#    """Your data serializer, define your fields here."""
#    data = serializers.FileField()
