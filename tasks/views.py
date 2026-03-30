from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required
from .models import Task
from .forms import TaskForm


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


@login_required
def add_task(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False) # พักไว้ก่อน อย่าเพิ่งลง DB
            task.owner = request.user      # แอบใส่เจ้าของงานให้เป็นคนที่ Login อยู่
            task.save()                    # ค่อยบันทึกลง DB จริงๆ
            return redirect('task_list')
    else:
        form = TaskForm()
    
    return render(request, 'tasks/task_form.html', {'form': form})


@login_required
def edit_task(request, task_id):
    # 1. ไปดึงงานชิ้นที่จะแก้ไขมา (ต้องเป็นเจ้าของด้วยนะ)
    task = get_object_or_404(Task, id=task_id, owner=request.user)
    
    if request.method == "POST":
        # 2. ถ้ากดบันทึก เอาข้อมูลใหม่ (request.POST) ไปทับข้อมูลเดิม (instance=task)
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        # 3. ถ้าเพิ่งเข้าหน้าเว็บ ให้เอาข้อมูลเดิมมาใส่รอไว้ในช่องกรอก
        form = TaskForm(instance=task)
    
    # ใช้ Template เดียวกับหน้า Add ได้เลย!
    return render(request, 'tasks/task_form.html', {'form': form, 'edit_mode': True})

@login_required
def update_status(request, task_id):
    task = get_object_or_404(Task, id=task_id, owner=request.user)
    
    if request.method == "POST":
        new_status = request.POST.get('status')
        
        # แทนที่จะเช็ก ['Todo', 'Done'] ให้เช็กจาก Choices ใน Model ตรงๆ
        # task.Status.values จะคืนค่าเป็น ['todo', 'pending', 'done'] ตามที่เราตั้งไว้
        if new_status in Task.Status.values:
            task.status = new_status
            task.save()
            
    return redirect('task_list')

@login_required
def task_detail(request: HttpRequest, task_id):
    task = get_object_or_404(Task, id=task_id, owner=request.user)

    context = {'task': task }
    return render(request, 'tasks/task_detail.html', context)