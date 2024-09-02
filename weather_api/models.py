from django.db import models

class Weather(models.Model):
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    temperature = models.FloatField()
    description = models.CharField(max_length=200)
    humidity = models.IntegerField()
    wind_speed = models.FloatField()
    pressure = models.FloatField()
    forecast = models.JSONField() 
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.city}, {self.country}"
