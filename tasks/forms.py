from django import forms
from .models import Task, PersonalData, Asistencia
from django.core.exceptions import ValidationError

# Formulario para Task
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'important']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'write a title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'write a description'}),
            'important': forms.CheckboxInput(attrs={'class': 'form-check-input text-center'}),
        }

# Formulario para PersonalData
class PersonalDataForm(forms.ModelForm):
    class Meta:
        model = PersonalData
        fields = '__all__'
        widgets = {
            'nombre_dueno': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del dueño'}),
            'nombre_mascota': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la mascota'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo'}),
            'asistencias': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }

class AsistenciaForm(forms.ModelForm):
    class Meta:
        model = Asistencia
        fields = ['cliente', 'dia_semana', 'hora_entrada', 'hora_salida']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'dia_semana': forms.Select(attrs={'class': 'form-control'}),
            'hora_entrada': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}, format='%H:%M'),
            'hora_salida': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}, format='%H:%M'),
        }

    def clean(self):
        cleaned_data = super().clean()
        dia = cleaned_data.get('dia_semana')

        if dia:
            from tasks.models import Asistencia
            cantidad = Asistencia.objects.filter(dia_semana=dia).count()
            if cantidad >= 50:
                raise ValidationError(f"Ya hay 50 asistencias registradas para {dia}. No se pueden registrar más.")

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super(AsistenciaForm, self).__init__(*args, **kwargs)
        for field in ['hora_entrada', 'hora_salida']:
            if self.instance and getattr(self.instance, field):
                self.fields[field].initial = getattr(self.instance, field).strftime('%H:%M')


