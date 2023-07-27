from django.contrib import admin

# Register your models here.
from .models import Certificate

@admin.register(Certificate)

class CertificateAdmin(admin.ModelAdmin):
    list_display = ("id","name",)