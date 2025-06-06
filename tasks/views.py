from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm
from .models import Task
from .forms import TaskForm, PersonalDataForm  
from .models import Task, PersonalData      
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .forms import AsistenciaForm
from .models import Asistencia
from django.contrib.auth.decorators import login_required
from django.db.models import Count

@login_required
def vista_privada(request):
    return render(request, 'privado.html')


# Create your views here.

def home(request):
    return render(request, 'home.html')

def contactos(request):
    return render(request, 'contactos.html')

def servicios(request):
    return render(request, 'servicios.html')

def quienes_somos(request):
    return render(request, 'quienes.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        codigo_ingresado = request.POST.get('codigo_acceso')
        codigo_correcto = 'PERRO2025'  # Código secreto válido

        # Validación del código secreto
        if codigo_ingresado != codigo_correcto:
            return render(request, 'signup.html', {
                'error': '⚠️ Código de invitación incorrecto.'
            })

        # Validación de contraseñas
        if password1 != password2:
            return render(request, 'signup.html', {
                'error': '⚠️ Las contraseñas no coinciden.'
            })

        # Intentar crear el usuario
        try:
            user = User.objects.create_user(username=username, password=password1)
            user.save()
            login(request, user)
            return redirect('tasks')
        except IntegrityError:
            return render(request, 'signup.html', {
                'error': '⚠️ El nombre de usuario ya existe.'
            })

    return render(request, 'signup.html')

@login_required
def tasks(request):
    tasks = Task.objects.filter(user = request.user, datecompleted__isnull=True)
    return render(request, 'tasks.html', {'tasks': tasks })

@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'tasks.html', {'tasks': tasks })

@login_required
def create_task(request):
    
    if request.method == 'GET':
        return render(request, 'create_task.html', {
            'form': TaskForm
        })
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'create_task.html', {
                'form': TaskForm,
                'error': 'please provide valid data'
            })
        
@login_required       
def task_detail(request, task_id):
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        form = TaskForm(instance=task)
        return render(request, 'task_detail.html', {'task': task, 'form': form})
    else:
        try:
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html', {'task': task,'form': form , 'error': 'Error updating task'})
    
@login_required   
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')
@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')
    
    
@login_required    
def signout(request):
    logout(request)
    return redirect('home')



def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'Username or password is incorrect'
                })
        else:
            login (request, user)
            return redirect('tasks')
        
def create_personal_data(request):
    if request.method == 'POST':
        form = PersonalDataForm(request.POST)
        if form.is_valid():
            personal_data = form.save(commit=False)  # No guarda aún
            personal_data.save()  # Ahora guarda el objeto sin ManyToMany
            form.save_m2m()  # Esto guarda las asistencias (ManyToMany)
            return redirect('lista_datos_personales')  # O la ruta que uses
    else:
        form = PersonalDataForm()
    
    return render(request, 'create_personal_data.html', {'form': form})

def asistencias_view(request):
    query = request.GET.get('q')
    
    if query:
        asistencias = Asistencia.objects.filter(cliente__nombre_dueno__icontains=query)
    else:
        asistencias = Asistencia.objects.all()

    return render(request, 'asistencias.html', {
        'asistencias': asistencias,
        'query': query,
    })

def crear_asistencia(request):
    if request.method == 'POST':
        form = AsistenciaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('asistencias')
    else:
        form = AsistenciaForm()
    return render(request, 'crear_asistencia.html', {'form': form})




def editar_asistencia(request, pk):
    asistencia = get_object_or_404(Asistencia, pk=pk)
    if request.method == 'POST':
        form = AsistenciaForm(request.POST, instance=asistencia)
        if form.is_valid():
            form.save()
            messages.success(request, "Asistencia actualizada exitosamente.")
            return redirect('asistencias')
    else:
        form = AsistenciaForm(instance=asistencia)
    return render(request, 'editar_asistencia.html', {'form': form})


def eliminar_asistencia(request, pk):
    asistencia = get_object_or_404(Asistencia, pk=pk)
    if request.method == 'POST':
        asistencia.delete()
        messages.success(request, "Asistencia eliminada exitosamente.")
        return redirect('asistencias')
    return render(request, 'eliminar_confirmacion.html', {'asistencia': asistencia})

def lista_datos_personales(request):
    clientes = PersonalData.objects.annotate(num_asistencias=Count('asistencias'))
    return render(request, 'lista_datos_personales.html', {'clientes': clientes})

def editar_datos_personales(request, id):
    cliente = get_object_or_404(PersonalData, id=id)

    if request.method == 'POST':
        form = PersonalDataForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('lista_datos_personales')  
    else:
        form = PersonalDataForm(instance=cliente)

    context = {
        'form': form,
        'cliente': cliente  
    }
    return render(request, 'editar_datos_personales.html', context)

def eliminar_datos_personales(request, id):
    cliente = get_object_or_404(PersonalData, id=id)
    if request.method == 'POST':
        cliente.delete()
        return redirect('lista_datos_personales')
    return render(request, 'confirmar_eliminar_cliente.html', {'cliente': cliente})