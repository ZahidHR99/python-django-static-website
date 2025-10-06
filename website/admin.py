from django.contrib import admin
from .models import *

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'designation', 'mobile', 'email', 'address', 'website', 'salary', 'is_active', 'created_at', 'updated_at')
    search_fields = ('name', 'email', 'mobile')
    ordering = ('-created_at',)
    date_hierarchy = ('created_at')
    list_display_links = ('name', 'email')
    list_per_page = 2
    list_max_show_all = 50
    readonly_fields = ('created_at', 'updated_at')
    list_editable = ('is_active',)
    list_filter = ('is_active', 'created_at')



admin.site.register(Employee, EmployeeAdmin)
admin.site.register(OTP)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Invoice)
admin.site.register(InvoiceProduct)
admin.site.register(Book)
admin.site.register(Project)
admin.site.register(Testimonial)
admin.site.register(ContactMessage)
admin.site.register(HireRequest)
admin.site.register(Demo)
admin.site.register(Download)
admin.site.register(BinaryResponse)
admin.site.register(About)
admin.site.register(Home)
admin.site.register(Author)
admin.site.register(Article)

# Register your models here.

