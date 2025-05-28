from django.contrib import admin
from django.urls import path
from tasks import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('tasks/', views.tasks, name='tasks'),
    path('tasks_completed/', views.tasks_completed, name='tasks_completed'),
    path('tasks/create/', views.create_task, name='create_task'),
    path('tasks/<int:task_id>/', views.task_detail, name='task_detail'),
    path('tasks/<int:task_id>/complete', views.complete_task, name='complete_task'),
    path('tasks/<int:task_id>/delete', views.delete_task, name='delete_task'),
    path('logout/', views.signout, name='logout'),
    path('signin/', views.signin, name='signin'),
    path('contactos/', views.contactos, name='contactos'),
    path('servicios/', views.servicios, name='servicios'),
    path('quienes/', views.quienes_somos, name='quienes'),
    path('datos-personales/', views.create_personal_data, name='create_personal_data'),
    path('asistencias/', views.asistencias_view, name='asistencias'),
    path('asistencias/nueva/', views.crear_asistencia, name='crear_asistencia'),
    path('asistencias/editar/<int:pk>/', views.editar_asistencia, name='editar_asistencia'),
    path('asistencias/eliminar/<int:pk>/', views.eliminar_asistencia, name='eliminar_asistencia'),
    path('clientes/', views.lista_datos_personales, name='lista_datos_personales'),
    path('clientes/editar/<int:id>/', views.editar_datos_personales, name='editar_datos_personales'),
    path('clientes/eliminar/<int:id>/', views.eliminar_datos_personales, name='eliminar_datos_personales'),
]



if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

