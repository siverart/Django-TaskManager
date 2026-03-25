from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required
from .models import Task

# Create your views here.
@login_required
def task_list(request: HttpRequest):
    tasks = Task.objects.filter(owner=request.user).order_by('deadline')
    context = {'tasks': tasks}
    return render(request, 'tasks/task_list.html', context)


@login_required
def delete_task(request, task_id):
    # ดึง Task ตาม id และต้องเป็น owner เท่านั้นถึงจะเห็น (ป้องกันคนแอบแก้ ID บน URL เพื่อลบงานคนอื่น)
    task = get_object_or_404(Task, id=task_id, owner=request.user)
    
    if request.method == "POST":
        task.delete()
        return redirect('task_list')
    
    # ถ้าไม่ได้ส่งมาเป็น POST (เช่น พิมพ์ URL ตรงๆ) ให้ดีดกลับไปหน้าเดิม
    return redirect('task_list')