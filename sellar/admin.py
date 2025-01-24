from django.contrib import admin
from .models import CustomUser, ManufacturerOrProductSeller, MachineVendor, ProfessionalWorker


class CustomUserAdmin(admin.ModelAdmin):
         list_display = ('username','user_type','is_active','is_staff','is_superuser')
         list_filter = ('user_type', 'is_active','is_staff','is_superuser')
         search_fields = ['username']

class ManufacturerAdmin(admin.ModelAdmin):
         list_display = ['user', 'company_name', 'unique_vendor_id','is_verified']
         list_filter = ['is_verified']
         search_fields = ['company_name','unique_vendor_id']

class MachineVendorAdmin(admin.ModelAdmin):
         list_display = ['user','unique_vendor_id','is_verified']
         list_filter = ['is_verified']
         search_fields = ['unique_vendor_id']

class ProfessionalWorkerAdmin(admin.ModelAdmin):
         list_display = ['user', 'category', 'unique_vendor_id','is_verified']
         list_filter = ['category','is_verified']
         search_fields = ['category','unique_vendor_id']

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(ManufacturerOrProductSeller, ManufacturerAdmin)
admin.site.register(MachineVendor, MachineVendorAdmin)
admin.site.register(ProfessionalWorker, ProfessionalWorkerAdmin)