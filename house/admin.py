from django.contrib import admin

from house import models


class HouseAdmin(admin.ModelAdmin):
    readonly_fields = ["id", "created_on"]


admin.site.register(models.House, HouseAdmin)
