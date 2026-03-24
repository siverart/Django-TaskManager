from django.contrib.auth.models import AbstractUser
from django.db import models
# Create your models here.


class CustomUser(AbstractUser):
    # ตอนนี้ยังไม่ต้องใส่ฟิลด์เพิ่มก็ได้ แต่การมี Class นี้ไว้ 
    # จะทำให้เราเพิ่มฟิลด์ในอนาคตได้ง่ายๆ ครับ
    pass