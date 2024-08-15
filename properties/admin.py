# admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import PropertyInfo, Image, Location, Amenity

class ImageInline(admin.TabularInline):
    model = Image
    extra = 1
    readonly_fields = ['image_preview']

    def image_preview(self, obj):
        if obj.img_path:
            return format_html('<img src="{}" width="70" height="70" />', obj.img_path.url)
        return "No Image"
    image_preview.short_description = 'Image Preview'

class PropertyInfoAdmin(admin.ModelAdmin):
    model = PropertyInfo
    inlines = [ImageInline]
    list_display = ('title', 'description', 'created_date', 'updated_date', 'display_locations', 'display_amenities', 'display_images')
    search_fields = ('title', 'description')
    filter_horizontal = ('amenities','locations',)

    def display_locations(self, obj):
        return ", ".join([f"{location.get_type_display()}: {location.name}" for location in obj.locations.all()])
    display_locations.short_description = 'Locations'

    def display_amenities(self, obj):
        return ", ".join([amenity.name for amenity in obj.amenities.all()])
    display_amenities.short_description = 'Amenities'

    def display_images(self, obj):
        return ", ".join([image.img_path.name for image in obj.images.all()])
    display_images.short_description = 'Images'

    def get_form(self, request, obj=None, **kwargs):
        form = super(PropertyInfoAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['amenities'].required = False
        return form

admin.site.register(PropertyInfo, PropertyInfoAdmin)
admin.site.register(Location)
admin.site.register(Amenity)
admin.site.register(Image)