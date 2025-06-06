from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count

# Modelo de tareas
class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True, blank=True)
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title + ' - by ' + self.user.username

class PersonalData(models.Model):
    nombre_dueno = models.CharField(max_length=100)
    nombre_mascota = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    correo = models.EmailField()
    

    def __str__(self):
        return f"{self.nombre_mascota} (Dueño: {self.nombre_dueno})"
    
class Asistencia(models.Model):
    DIA_SEMANA_CHOICES = [
        ('Lunes', 'Lunes'),
        ('Martes', 'Martes'),
        ('Miércoles', 'Miércoles'),
        ('Jueves', 'Jueves'),
        ('Viernes', 'Viernes'),
        ('Sábado', 'Sábado'),
        ('Domingo', 'Domingo'),
    ]

    cliente = models.ForeignKey(PersonalData, on_delete=models.CASCADE, related_name='asistencias')
    dia_semana = models.CharField(max_length=10, choices=DIA_SEMANA_CHOICES)
    hora_entrada = models.TimeField(null=True, blank=True)
    hora_salida = models.TimeField(null=True, blank=True)

    
    def __str__(self):
        return f"{self.dia_semana} - Entrada: {self.hora_entrada} | Salida: {self.hora_salida}"

