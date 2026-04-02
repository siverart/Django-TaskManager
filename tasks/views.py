from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required
from .models import Task
from .forms import TaskForm
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import TaskSerializer
from tasks import serializers
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

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


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def get_tasks(request):

    # GET
    if request.method == 'GET':
        tasks = Task.objects.filter(owner=request.user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)
    
    # POST
    elif request.method == 'POST':
        serializer = TaskSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk, owner=request.user)
    serializer = TaskSerializer(task)
    return Response(serializer.data)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_task(request, pk):
    task = get_object_or_404(Task, pk=pk, owner=request.user)

    if request.method == 'PUT':
        serializer = TaskSerializer(task, data=request.data)

    elif request.method == 'PATCH':
        serializer = TaskSerializer(task, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk, owner=request.user)

    task.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)