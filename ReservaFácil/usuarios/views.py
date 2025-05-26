from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import RegistroForm, LoginForm

# Create your views here.

class RegistroView(CreateView):
    form_class = RegistroForm
    template_name = 'usuarios/registro.html'
    success_url = reverse_lazy('usuarios:login')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, '¡Cuenta creada exitosamente! Ahora puedes iniciar sesión.')
        return response
    
    def form_invalid(self, form):
        messages.error(self.request, 'Por favor corrige los errores en el formulario.')
        return super().form_invalid(form)

class CustomLoginView(LoginView):
    form_class = LoginForm
    template_name = 'usuarios/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        """Personalizar la URL de redirección después del login exitoso"""
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        return reverse_lazy('inicio')
    
    def form_valid(self, form):
        """Manejar login exitoso"""
        user = form.get_user()
        login(self.request, user)
        
        # Verificar que el usuario tenga perfil
        if hasattr(user, 'perfilusuario'):
            tipo_usuario = user.perfilusuario.get_tipo_usuario_display()
            messages.success(
                self.request, 
                f'¡Bienvenido, {user.get_full_name() or user.username}! ({tipo_usuario})'
            )
        else:
            messages.success(
                self.request, 
                f'¡Bienvenido, {user.get_full_name() or user.username}!'
            )
        
        return redirect(self.get_success_url())
    
    def form_invalid(self, form):
        """Manejar errores de login"""
        messages.error(self.request, 'Credenciales inválidas. Por favor verifica tu usuario y contraseña.')
        return super().form_invalid(form)

class CustomLogoutView(LogoutView):
    next_page = 'inicio'  # Redirigir a la página de inicio después del logout
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            username = request.user.get_full_name() or request.user.username
            response = super().dispatch(request, *args, **kwargs)
            messages.info(request, f'Hasta luego, {username}! Has cerrado sesión exitosamente.')
            return response
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        """Permitir logout con método GET para compatibilidad"""
        return self.post(request, *args, **kwargs)
