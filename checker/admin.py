from django.contrib import admin

from checker.models import UploadedFile


# Register your models here.
@admin.register(UploadedFile)
class UploadedFileAdmin(admin.ModelAdmin):
    pass
