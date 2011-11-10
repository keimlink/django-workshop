from django.contrib import admin

from addressbook.models import Address, City


class AddressAdmin(admin.ModelAdmin):
    actions = None
    list_display = ('first_name', 'last_name', 'street', 'zipcode', 'city')
    list_display_links = ('first_name', 'last_name')
    list_filter = ('city',)
    search_fields = ['first_name', 'last_name', 'street', 'zipcode', 'city']
    readonly_fields = ('first_name', 'last_name', 'street', 'zipcode', 'city')


admin.site.register(Address, AddressAdmin)
admin.site.register(City)
