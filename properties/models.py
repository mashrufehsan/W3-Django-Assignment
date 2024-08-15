from django.db import models
from django.utils import timezone

class Location(models.Model):
    COUNTRY = 'country'
    STATE = 'state'
    CITY = 'city'
    TYPE_CHOICES = [
        (COUNTRY, 'Country'),
        (STATE, 'State'),
        (CITY, 'City'),
    ]
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_type_display()}: {self.name}"

    class Meta:
        db_table = 'location'
        verbose_name_plural = 'Locations'

class Amenity(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'amenity'
        verbose_name_plural = 'Amenities'

class PropertyInfo(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    locations = models.ManyToManyField(Location, related_name='properties')
    amenities = models.ManyToManyField(Amenity, related_name='properties')
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'property_info'
        verbose_name_plural = 'Property Info'

class Image(models.Model):
    property_info = models.ForeignKey(PropertyInfo, related_name='images', on_delete=models.CASCADE)
    img_path = models.ImageField(upload_to='images/', max_length=255)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.img_path.name

    class Meta:
        db_table = 'image'
        verbose_name_plural = 'Images'
