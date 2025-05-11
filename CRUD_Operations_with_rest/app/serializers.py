from rest_framework import serializers
from app.models import Database

class Serializer_Database(serializers.ModelSerializer):
    class Meta:
        model = Database
        fields="__all__"