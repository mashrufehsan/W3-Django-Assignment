import os
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.utils import timezone


def generate_image_filename(instance, filename):
    ext = filename.split('.')[-1]
    timestamp = timezone.now().strftime("%Y%m%d_%H%M%S_%f")
    filename = f"{timestamp}.{ext}"
    return os.path.join('images', filename)


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
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_type_display()}: {self.name}"

    class Meta:
        unique_together = ('name', 'type')
        db_table = 'location'
        verbose_name_plural = 'Locations'


class Amenity(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'amenity'
        verbose_name_plural = 'Amenities'


class PropertyInfo(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
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
    property_info = models.ForeignKey(
        PropertyInfo, related_name='images', on_delete=models.CASCADE)
    img_path = models.ImageField(
        upload_to=generate_image_filename, max_length=255)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.img_path.name

    def delete(self, *args, **kwargs):
        if self.img_path:
            if os.path.isfile(self.img_path.path):
                os.remove(self.img_path.path)
        super(Image, self).delete(*args, **kwargs)

    class Meta:
        db_table = 'image'
        verbose_name_plural = 'Images'


@receiver(pre_delete, sender=Image)
def delete_image_file(sender, instance, **kwargs):
    if instance.img_path:
        if os.path.isfile(instance.img_path.path):
            os.remove(instance.img_path.path)
