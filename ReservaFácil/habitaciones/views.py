from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Habitacion
from .forms import HabitacionForm, BusquedaHabitacionForm, ConsultaDisponibilidadForm

class PersonalAutorizadoMixin(UserPassesTestMixin):
    """Mixin para verificar que el usuario sea personal autorizado (recepción o administrador)"""
    
    def test_func(self):
        if not self.request.user.is_authenticated:
            return False
        
        # Verificar si el usuario tiene perfil y es personal autorizado
        if hasattr(self.request.user, 'perfilusuario'):
            perfil = self.request.user.perfilusuario
            return perfil.es_personal_recepcion() or perfil.es_administrador()
        
        # Si no tiene perfil pero es staff o superuser, permitir acceso
        return self.request.user.is_staff or self.request.user.is_superuser
    
    def handle_no_permission(self):
        messages.error(self.request, 'No tienes permisos para acceder a esta sección.')
        return redirect('inicio')

def consultar_disponibilidad(request):
    """Vista para consultar disponibilidad de habitaciones por fechas"""
    form = ConsultaDisponibilidadForm()
    habitaciones_disponibles = []
    mostrar_resultados = False
    total_noches = 0
    
    if request.method == 'POST':
        form = ConsultaDisponibilidadForm(request.POST)
        if form.is_valid():
            fecha_entrada = form.cleaned_data['fecha_entrada']
            fecha_salida = form.cleaned_data['fecha_salida']
            tipo_habitacion = form.cleaned_data.get('tipo_habitacion')
            capacidad_minima = form.cleaned_data.get('capacidad_minima')
            
            # Calcular número de noches
            total_noches = (fecha_salida - fecha_entrada).days
            
            # Filtrar habitaciones disponibles
            queryset = Habitacion.objects.filter(estado='disponible')
            
            # Aplicar filtros adicionales si se proporcionan
            if tipo_habitacion:
                queryset = queryset.filter(tipo=tipo_habitacion)
            
            if capacidad_minima:
                queryset = queryset.filter(capacidad__gte=capacidad_minima)
            
            # TODO: Aquí se debería verificar que no haya reservas confirmadas
            # para el rango de fechas. Por ahora solo verificamos el estado.
            habitaciones_disponibles = queryset.order_by('precio_por_noche')
            mostrar_resultados = True
            
            if habitaciones_disponibles:
                messages.success(
                    request, 
                    f'Se encontraron {habitaciones_disponibles.count()} habitaciones disponibles '
                    f'para {total_noches} noche{"s" if total_noches != 1 else ""}.'
                )
            else:
                messages.warning(
                    request,
                    'No se encontraron habitaciones disponibles para las fechas seleccionadas.'
                )
    
    context = {
        'form': form,
        'habitaciones_disponibles': habitaciones_disponibles,
        'mostrar_resultados': mostrar_resultados,
        'total_noches': total_noches,
    }
    
    return render(request, 'habitaciones/consultar_disponibilidad.html', context)

class HabitacionListView(PersonalAutorizadoMixin, ListView):
    model = Habitacion
    template_name = 'habitaciones/lista.html'
    context_object_name = 'habitaciones'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = Habitacion.objects.all()
        form = BusquedaHabitacionForm(self.request.GET)
        
        if form.is_valid():
            numero = form.cleaned_data.get('numero')
            tipo = form.cleaned_data.get('tipo')
            estado = form.cleaned_data.get('estado')
            
            if numero:
                queryset = queryset.filter(numero__icontains=numero)
            if tipo:
                queryset = queryset.filter(tipo=tipo)
            if estado:
                queryset = queryset.filter(estado=estado)
        
        return queryset.order_by('numero')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_busqueda'] = BusquedaHabitacionForm(self.request.GET)
        context['total_habitaciones'] = Habitacion.objects.count()
        context['habitaciones_disponibles'] = Habitacion.objects.filter(estado='disponible').count()
        return context

class HabitacionCreateView(PersonalAutorizadoMixin, CreateView):
    model = Habitacion
    form_class = HabitacionForm
    template_name = 'habitaciones/crear.html'
    success_url = reverse_lazy('habitaciones:lista')
    
    def form_valid(self, form):
        messages.success(self.request, f'Habitación {form.instance.numero} creada exitosamente.')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Por favor corrige los errores en el formulario.')
        return super().form_invalid(form)

class HabitacionUpdateView(PersonalAutorizadoMixin, UpdateView):
    model = Habitacion
    form_class = HabitacionForm
    template_name = 'habitaciones/editar.html'
    success_url = reverse_lazy('habitaciones:lista')
    
    def form_valid(self, form):
        messages.success(self.request, f'Habitación {form.instance.numero} actualizada exitosamente.')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Por favor corrige los errores en el formulario.')
        return super().form_invalid(form)

class HabitacionDeleteView(PersonalAutorizadoMixin, DeleteView):
    model = Habitacion
    template_name = 'habitaciones/eliminar.html'
    success_url = reverse_lazy('habitaciones:lista')
    
    def delete(self, request, *args, **kwargs):
        habitacion = self.get_object()
        messages.success(request, f'Habitación {habitacion.numero} eliminada exitosamente.')
        return super().delete(request, *args, **kwargs)

@login_required
def detalle_habitacion(request, pk):
    """Vista para ver los detalles de una habitación"""
    habitacion = get_object_or_404(Habitacion, pk=pk)
    
    # Verificar permisos
    if hasattr(request.user, 'perfilusuario'):
        perfil = request.user.perfilusuario
        if not (perfil.es_personal_recepcion() or perfil.es_administrador()):
            messages.error(request, 'No tienes permisos para ver esta información.')
            return redirect('inicio')
    elif not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, 'No tienes permisos para ver esta información.')
        return redirect('inicio')
    
    return render(request, 'habitaciones/detalle.html', {'habitacion': habitacion})
