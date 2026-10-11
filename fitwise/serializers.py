from rest_framework import serializers
from django.contrib.auth.models import User
from datetime import date
from .models import FoodLog



class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["username","email","password"]
        read_only_fields = ["id"]

        
class FoodLogSerializer(serializers.ModelSerializer):

    class Meta:
        model = FoodLog
        fields = "__all__"
        read_only_fields = ["id","owner","created_at","updated_at",]

    def validate_date(self, value):
        if value > date.today():
            raise serializers.ValidationError("You cannot record food for a future date.")
        return value