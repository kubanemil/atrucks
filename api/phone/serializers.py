from rest_framework import serializers

from .models import PhoneInfo


class PhoneInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneInfo
        fields = "__all__"
