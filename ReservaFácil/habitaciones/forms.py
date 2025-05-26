from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import date
from .models import Habitacion

class HabitacionForm(forms.ModelForm):
    class Meta:
        model = Habitacion
        fields = ['numero', 'tipo', 'precio_por_noche', 'capacidad', 'servicios_incluidos', 'estado', 'descripcion']
        widgets = {
            'numero': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 101, 201A'
            }),
            'tipo': forms.Select(attrs={
                'class': 'form-select'
            }),
            'precio_por_noche': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Precio en pesos colombianos',
                'step': '0.01',
                'min': '0.01'
            }),
            'capacidad': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número de huéspedes',
                'min': '1'
            }),
            'servicios_incluidos': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Ej: WiFi gratuito, TV cable, minibar, aire acondicionado...'
            }),
            'estado': forms.Select(attrs={
                'class': 'form-select'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descripción adicional de la habitación...'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hacer que algunos campos sean requeridos
        self.fields['numero'].required = True
        self.fields['tipo'].required = True
        self.fields['precio_por_noche'].required = True
        self.fields['capacidad'].required = True
        
        # Agregar clases CSS para validación
        for field_name, field in self.fields.items():
            if field.required:
                field.widget.attrs['required'] = True

class BusquedaHabitacionForm(forms.Form):
    numero = forms.CharField(
        max_length=10,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Número de habitación'
        })
    )
    tipo = forms.ChoiceField(
        choices=[('', 'Todos los tipos')] + Habitacion.TIPOS_HABITACION,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    estado = forms.ChoiceField(
        choices=[('', 'Todos los estados')] + Habitacion.ESTADOS_HABITACION,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )

class ConsultaDisponibilidadForm(forms.Form):
    fecha_entrada = forms.DateField(
        label="Fecha de Entrada",
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'placeholder': 'dd/mm/aaaa'
        }),
        help_text="Selecciona la fecha de llegada"
    )
    fecha_salida = forms.DateField(
        label="Fecha de Salida",
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'placeholder': 'dd/mm/aaaa'
        }),
        help_text="Selecciona la fecha de salida"
    )
    tipo_habitacion = forms.ChoiceField(
        label="Tipo de Habitación",
        choices=[('', 'Cualquier tipo')] + Habitacion.TIPOS_HABITACION,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select'
        }),
        help_text="Filtra por tipo de habitación (opcional)"
    )
    capacidad_minima = forms.IntegerField(
        label="Capacidad Mínima",
        min_value=1,
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Número de huéspedes',
            'min': '1'
        }),
        help_text="Número mínimo de huéspedes (opcional)"
    )

    def clean_fecha_entrada(self):
        fecha_entrada = self.cleaned_data.get('fecha_entrada')
        
        if fecha_entrada and fecha_entrada < date.today():
            raise ValidationError(
                "La fecha de entrada no puede ser anterior al día actual."
            )
        
        return fecha_entrada

    def clean_fecha_salida(self):
        fecha_salida = self.cleaned_data.get('fecha_salida')
        
        if fecha_salida and fecha_salida < date.today():
            raise ValidationError(
                "La fecha de salida no puede ser anterior al día actual."
            )
        
        return fecha_salida

    def clean(self):
        cleaned_data = super().clean()
        fecha_entrada = cleaned_data.get('fecha_entrada')
        fecha_salida = cleaned_data.get('fecha_salida')

        if fecha_entrada and fecha_salida:
            if fecha_entrada >= fecha_salida:
                raise ValidationError(
                    "La fecha de entrada debe ser anterior a la fecha de salida."
                )
            
            # Validar que no sea una estancia demasiado larga (opcional)
            diferencia_dias = (fecha_salida - fecha_entrada).days
            if diferencia_dias > 365:
                raise ValidationError(
                    "La estancia no puede ser mayor a 365 días."
                )

        return cleaned_data 