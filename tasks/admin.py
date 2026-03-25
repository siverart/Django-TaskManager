from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    # บอกให้หน้า Admin โชว์คอลัมน์อะไรบ้าง
    list_display = ('task_name', 'priority', 'status', 'owner', 'deadline')
    # เพิ่มตัวกรอง (Filter) ข้างๆ หน้าจอ
    list_filter = ('priority', 'status')
    #ใช้ในการค้นหา
    search_fields = ('task_name', 'description')