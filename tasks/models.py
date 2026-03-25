from django.db import models
from django.conf import settings # แนะนำให้ดึง User Model ผ่าน settings

class Task(models.Model):
    # 1. Choices สำหรับ Priority และ Status (สร้างเป็น Class จะดูโปรและจัดการง่ายครับ)
    class Priority(models.IntegerChoices):
        HIGH = 3, "ด่วนมาก"
        MEDIUM = 2, "ปกติ"
        LOW = 1, "ไม่เร่งด่วน"

    class Status(models.TextChoices):
        TODO = 'todo', "To Do"
        IN_PROGRESS = 'in_progress', "In Progress"
        PENDING = 'pending', "Pending"
        DONE = 'done', "Done"

    # 2. Fields ตามที่คุณระบุ
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="tasks",
        verbose_name="เจ้าของงาน"
    )
    task_name = models.CharField(max_length=255, verbose_name="ชื่อหัวข้องาน")
    description = models.TextField(null=True, blank=True, verbose_name="รายละเอียดงาน")
    category = models.CharField(max_length=100, verbose_name="ประเภทงาน") # User พิมพ์เอง
    
    deadline = models.DateTimeField(null=True, blank=True, verbose_name="กำหนดส่ง")
    
    priority = models.IntegerField(
        choices=Priority.choices, 
        default=Priority.MEDIUM,
        verbose_name="ความเร่งด่วน"
    )
    
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.TODO,
        verbose_name="สถานะ"
    )

    # 3. Time Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name="วันที่เสร็จงาน")

    class Meta:
        ordering = ['-priority', 'deadline'] # เรียงตามความด่วน และวันกำหนดส่ง
        verbose_name = "งาน"
        verbose_name_plural = "รายการงานทั้งหมด"

    def __str__(self):
        return f"{self.task_name} ({self.get_status_display()})"


