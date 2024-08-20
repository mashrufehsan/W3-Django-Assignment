from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import PropertyInfo, Image, Location, Amenity


class ImageInline(admin.TabularInline):
    model = Image
    extra = 1
    readonly_fields = ['image_preview', 'created_date', 'updated_date']

    def image_preview(self, obj):
        if obj.img_path:
            return format_html('<img src="{}" width="100" height="100"/>', obj.img_path.url)
        return "No Image"
    image_preview.short_description = 'Image Preview'


class PropertyInfoAdmin(admin.ModelAdmin):
    model = PropertyInfo
    inlines = [ImageInline]
    list_display = ('title', 'description', 'created_date', 'updated_date',
                    'display_locations', 'display_amenities', 'display_images')
    search_fields = ['title', 'description', 'locations__name']
    filter_horizontal = ['amenities', 'locations']
    readonly_fields = ['created_date', 'updated_date']
    list_filter = ['amenities', 'created_date', 'updated_date']

    def display_locations(self, obj):
        return ", ".join([f"{location.get_type_display()}: {location.name}" for location in obj.locations.all()])
    display_locations.short_description = 'Locations'

    def display_amenities(self, obj):
        return ", ".join([amenity.name for amenity in obj.amenities.all()])
    display_amenities.short_description = 'Amenities'

    def display_images(self, obj):
        images = obj.images.all()[:3]
        image_tags = [
            f'<img src="{image.img_path.url}" width="50" height="50" style="margin-right: 5px;"/>' for image in images]
        more_indicator = '[continued...]' if obj.images.count() > 3 else ''
        return mark_safe(''.join(image_tags) + more_indicator)
    display_images.short_description = 'Images'

    def get_form(self, request, obj=None, **kwargs):
        form = super(PropertyInfoAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['amenities'].required = False
        return form


class ImageAdmin(admin.ModelAdmin):
    list_display = ('img_path', 'image_preview', 'property_info_title',
                    'change_link', 'created_date', 'updated_date')
    readonly_fields = ['image_preview', 'created_date', 'updated_date']
    search_fields = ['property_info__title']
    list_filter = ['created_date', 'updated_date']

    def image_preview(self, obj):
        if obj.img_path:
            return format_html('<img src="{}" width="100" height="100" />', obj.img_path.url)
        return "No Image"
    image_preview.short_description = 'Image Preview'

    def property_info_title(self, obj):
        return obj.property_info.title
    property_info_title.short_description = 'Property Info Title'

    def change_link(self, obj):
        url = reverse('admin:properties_image_change', args=[obj.pk])
        return format_html('<a href="{}">Edit</a>', url)
    change_link.short_description = 'Edit Image'


class AmenityAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_date', 'updated_date')
    readonly_fields = ['created_date', 'updated_date']
    search_fields = ['name']
    list_filter = ['created_date', 'updated_date']


class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'latitude',
                    'longitude', 'created_date', 'updated_date')
    readonly_fields = ['created_date', 'updated_date']
    search_fields = ['name', 'type']
    list_filter = ['type', 'created_date', 'updated_date']


admin.site.register(PropertyInfo, PropertyInfoAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Amenity, AmenityAdmin)
admin.site.register(Image, ImageAdmin)
