from django.urls import path
from .views import (
    HabitacionListView, 
    HabitacionCreateView, 
    HabitacionUpdateView, 
    HabitacionDeleteView,
    detalle_habitacion,
    consultar_disponibilidad
)

app_name = 'habitaciones'

urlpatterns = [
    path('', HabitacionListView.as_view(), name='lista'),
    path('disponibilidad/', consultar_disponibilidad, name='consultar_disponibilidad'),
    path('crear/', HabitacionCreateView.as_view(), name='crear'),
    path('<int:pk>/', detalle_habitacion, name='detalle'),
    path('<int:pk>/editar/', HabitacionUpdateView.as_view(), name='editar'),
    path('<int:pk>/eliminar/', HabitacionDeleteView.as_view(), name='eliminar'),
] 