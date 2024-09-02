from rest_framework import serializers

class WeatherSerializer(serializers.Serializer):
    city = serializers.CharField(max_length=100)
    country = serializers.CharField(max_length=100)
    temperature = serializers.FloatField()
    description = serializers.CharField(max_length=200)
    humidity = serializers.IntegerField()
    wind_speed = serializers.FloatField()
    pressure = serializers.FloatField()
    forecast = serializers.ListField(child=serializers.DictField())