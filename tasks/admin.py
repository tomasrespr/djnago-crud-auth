from django.contrib import admin
from .models import Task, PersonalData
from .models import Asistencia

class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)

    class Media:
        css = {
            'all': ('css/admin.css',)
        }

class AsistenciaAdmin(admin.ModelAdmin):
    list_display = ('dia_semana', 'fecha_entrada', 'fecha_salida')

admin.site.register(Task, TaskAdmin)
admin.site.register(PersonalData)
admin.site.register(Asistencia)



