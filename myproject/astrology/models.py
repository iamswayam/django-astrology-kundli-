from django.db import models
from timezonefinder import TimezoneFinder

class KundliDetails(models.Model):
    name = models.CharField(max_length=100)
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    birth_date = models.DateField()
    birth_time = models.TimeField()
    place_of_birth = models.CharField(max_length=100)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    TIMEZONE_CHOICES = [
        ('Asia/Kolkata', 'Asia/Kolkata'),
        ('UTC', 'UTC'),
        ('America/New_York', 'America/New_York'),
        ('Europe/London', 'Europe/London'),
        # Add more as needed
    ]
    timezone = models.CharField(max_length=50, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.place_of_birth and (self.latitude is None or self.longitude is None or not self.timezone):
            from geopy.geocoders import Nominatim
            geolocator = Nominatim(user_agent="myapp")
            location = geolocator.geocode(self.place_of_birth, addressdetails=True)
            if location:
                self.latitude = location.latitude
                self.longitude = location.longitude
                address = location.raw.get('address', {})
                city = address.get('city') or address.get('town') or address.get('village') or ''
                state = address.get('state') or ''
                country = address.get('country') or ''
                parts = [part for part in [city, state, country] if part]
                self.place_of_birth = ', '.join(parts)
                # Get timezone from latitude and longitude
                tf = TimezoneFinder()
                self.timezone = tf.timezone_at(lng=self.longitude, lat=self.latitude)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Kundli Details"