from django.contrib import admin
from .models import Task, PersonalData, Asistencia

class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)

    class Media:
        css = {
            'all': ('css/admin.css',)
        }

@admin.register(PersonalData)
class PersonalDataAdmin(admin.ModelAdmin):
    list_display = ('nombre_dueno', 'nombre_mascota', 'telefono', 'correo')
    search_fields = ('nombre_dueno', 'nombre_mascota', 'correo')

@admin.register(Asistencia)
class AsistenciaAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'dia_semana', 'hora_entrada', 'hora_salida')
    search_fields = ('cliente__nombre_dueno', 'cliente__nombre_mascota')
    list_filter = ('dia_semana',)


admin.site.register(Task, TaskAdmin)



