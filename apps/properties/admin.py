from django.contrib import admin

from apps.properties.models import PropertyTypes, Property, StreetTypes


# Register your models here.

class PropertyTypesAdmin(admin.ModelAdmin):
    list_display = ['id', 'type_name','is_active']
    search_fields = ['id', 'type_name']
    list_filter = ['is_active']
    ordering = ['id', ]

class StreetTypesAdmin(admin.ModelAdmin):
    list_display = ['id', 'type_name','is_active']
    search_fields = ['id', 'type_name']
    list_filter = ['is_active']
    ordering = ['id', ]

class PropertyAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'street_name', 'street_type', 'suffix', 'suburb', 'postcode', 'state', 'is_active']
    list_filter = ['is_active', 'street_type']
    search_fields = ['id', 'customer__customer__name', 'street_name', 'suffix']
    ordering = ['id', ]


admin.site.register(PropertyTypes, PropertyTypesAdmin)
admin.site.register(StreetTypes, StreetTypesAdmin)
admin.site.register(Property, PropertyAdmin)
