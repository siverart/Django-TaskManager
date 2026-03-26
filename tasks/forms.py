from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        # เลือกฟิลด์ที่อยากให้ User กรอก (ไม่ต้องเอา owner มา เพราะเราจะใส่ให้เองใน View)
        fields = ['task_name', 'description', 'deadline', 'priority', 'category']
        
        # ใส่ "เสื้อผ้า" (CSS Class) ให้ช่องกรอกข้อมูลผ่าน Widgets
        widgets = {
            'task_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ชื่อ งานของคุณ'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'deadline': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'category': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'เช่น งานส่วนตัว, งานบริษัท'}),
        }