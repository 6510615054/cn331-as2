from django.contrib import admin
from myapp.models import Student,Subject,Register,TempRegister

# Register your models here.
admin.site.register(Student)
admin.site.register(Subject)
admin.site.register(Register)
admin.site.register(TempRegister)

# class RegisterAdmin(admin.ModelAdmin):
#     # ทำให้ทุกฟิลด์เป็น read-only
#     readonly_fields = [field.name for field in Register._meta.fields]  

#     def has_add_permission(self, request):
#         return False  # ปิดการเพิ่ม

#     def has_change_permission(self, request, obj=None):
#         return False  # ปิดการแก้ไข

#     def has_delete_permission(self, request, obj=None):
#         return False  # ปิดการลบ

# # ลงทะเบียนโมเดล Register กับ admin
# admin.site.register(Register, RegisterAdmin)