from django.contrib import admin

from .models import Address, City


class AddressAdmin(admin.ModelAdmin):
    actions = None
    list_display = ('first_name', 'last_name', 'street', 'zipcode', 'city')
    list_display_links = ('first_name', 'last_name')
    list_filter = ('city', 'last_name')
    search_fields = ['first_name', 'last_name', 'street', 'zipcode', 'city__name']
    readonly_fields = ('first_name', 'last_name', 'street', 'zipcode', 'city')


admin.site.register(Address, AddressAdmin)
admin.site.register(City)
