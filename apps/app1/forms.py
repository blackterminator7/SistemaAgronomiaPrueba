from django import forms
from .models import *
from django.contrib.admin.widgets import AdminDateWidget
from django.contrib.postgres.fields import ArrayField

sexo = [('M', 'M'), ('F', 'F'), ]
estado = [('Aceptado', 'Aceptado'), ('Denegado', 'Denegado')]


class CicloForm(forms.ModelForm):
    class Meta:
        model = Ciclo
        widgets = {
            'codigo_ciclo': forms.TextInput(attrs={'placeholder': 'Código Ciclo', 'autofocus': '', 'required': '', 'maxlength':'5', 'pattern': '[1-2]{1}[0-9]{4}', 'title': 'Ingreselo con el formato Numero de Ciclo (1 o 2) y Año calendario,   Ej: 12020. (Esto significa el Ciclo 1, del Año 2020)'}),
        }
        fields = {
            'codigo_ciclo': forms.IntegerField,
        }
        labels = {
            'codigo_ciclo': 'Codigo Ciclo',
        }

    def __init__(self, *args, **kwargs):
        super(CicloForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
                })
                


#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


class  EstudianteForm(forms.ModelForm):
    class Meta:
        model = Estudiante
        widgets = {
            'carnet_estudiante': forms.TextInput(attrs={'placeholder': 'Carnet Estudiante', 'autofocus': '', 'required': '', 'maxlength':'7', 'pattern': '([a-zA-Z]{2}[0-9]{5})', 'title': 'Ingrese el Carnet, Ej. AA99999.'}),
            'telefono_estudiante': forms.TextInput(attrs={'placeholder': 'Telefono Estudiante', 'autofocus': '', 'required': '', 'autocomplete': 'off', 'maxlength':'15', 'pattern': '[0-9]{8,15}', 'title': 'Ingrese el Telefono, Solo Numeros Enteros Sin Espacio.'}),
            'correo_estudiante': forms.TextInput(attrs={'placeholder': 'Correo Estudiante', 'autofocus': '', 'required': '', 'autocomplete': 'off', 'pattern': '^[a-z0-9!#$%&*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$'}),
            'nombre_estudiante': forms.TextInput(attrs={'placeholder': 'Nombres Estudiante', 'autofocus': '', 'autocomplete': 'off', 'required': '', 'maxlength':'50'}),
            'apellido_estudiante': forms.TextInput(attrs={'placeholder': 'Apellidos Estudiante', 'autofocus': '', 'autocomplete': 'off', 'required': '', 'maxlength':'50'}),
            'direccion_estudiante': forms.TextInput(attrs={'placeholder': 'Direccion Estudiante', 'autofocus': '', 'required': ''}),
            'sexo_estudiante': forms.Select(choices=sexo),
        }
        fields = {
            'carnet_estudiante': forms.CharField,
            'nombre_estudiante': forms.CharField,
            'apellido_estudiante': forms.CharField,
            'sexo_estudiante': forms.CharField,
            'telefono_estudiante': forms.IntegerField,
            'correo_estudiante': forms.CharField,
            'direccion_estudiante': forms.CharField,
        }
        labels = {
            'carnet_estudiante': 'Carnet',
            'nombre_estudiante':'Nombre',
            'apellido_estudiante':'Apellido',
            'sexo_estudiante': 'Sexo',
            'telefono_estudiante': 'Telefono',
            'correo_estudiante': 'Correo',
            'direccion_estudiante': 'Direccion',
        }

    def __init__(self, *args, **kwargs):
        super(EstudianteForm, self).__init__(*args, **kwargs)

        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'material-control tooltips-general'
                })

        self.fields['sexo_estudiante'].widget.attrs.update({
                'class': 'form-control'
                })


#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


class EstudioUniversitarioForm(forms.ModelForm):
    codigo_carrera = forms.ModelChoiceField(queryset=Carrera.objects.all().order_by('nombre_carrera'))
    codigo_ciclo = forms.ModelChoiceField(queryset=Ciclo.objects.all().order_by('codigo_ciclo'))
    carnet_estudiante = forms.ModelChoiceField(queryset=Estudiante.objects.all().order_by('carnet_estudiante'))

    class Meta:
        model = EstudioUniversitario
        widgets = {
            'porc_carrerar_aprob': forms.TextInput(attrs={'placeholder': 'Porcentaje Carrera Aprobado', 'autofocus': '', 'required': '', 'maxlength':'3', 'pattern': '([0-9]{1,3})', 'title': 'Ingrese el Pocentaje de Carrera Aprobado, Solo Numeros Enteros, No Coloque Signo de %.'}),
            'unidades_valorativas': forms.TextInput(attrs={'placeholder': 'Unidades Valorativas', 'autofocus': '', 'required': '',  'maxlength':'3', 'pattern': '([0-9]{1,3})', 'title': 'Ingrese la Cantidad de Unidades Valorativas Obtenidas.'}),
            'experiencia_areas_conoc': forms.TextInput(attrs={'placeholder': 'Experiencia en Areas Conocidas', 'autofocus': '', 'maxlength':'200', 'title': 'Si no tiene ninguna experiencia porfavor escriba "Ninguna".'}),
        }
        fields = {
            'carnet_estudiante': forms.CharField,
            'codigo_carrera': forms.CharField,
            'codigo_ciclo': forms.IntegerField,
            'porc_carrerar_aprob': forms.IntegerField,
            'unidades_valorativas': forms.IntegerField,
            'experiencia_areas_conoc': forms.CharField,
        }
        labels = {
            'carnet_estudiante': 'Carnet Estudiante',
            'codigo_carrera': 'Carrera Estudiante',
            'codigo_ciclo': 'Ciclo',
            'porc_carrerar_aprob': 'Porcentaje Carrera Aprobado',
            'unidades_valorativas': 'Unidades Valorativas',
            'experiencia_areas_conoc': 'Experiencia en Areas Conocidas',
        }

    def __init__(self, *args, **kwargs):
        super(EstudioUniversitarioForm, self).__init__(*args, **kwargs)

        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'material-control tooltips-general'
                })

        self.fields['carnet_estudiante'].widget.attrs.update({
                'class': 'form-control',
                'data-toggle': 'tooltip',
                'data-html': 'true',
                'data-placement': 'right',
                'title': 'Busca tu carnet en la siguiente lista, estos están ordenados en forma ascendente para una búsqueda más rápida. Por favor verifica que hayas seleccionado tu carnet correctamente.'
                })
        self.fields['codigo_carrera'].widget.attrs.update({
                'class': 'form-control',
                'data-toggle': 'tooltip',
                'data-html': 'true',
                'data-placement': 'right',
                'title': 'Selecciona la carrera a la que perteneces.'
                })
        self.fields['codigo_ciclo'].widget.attrs.update({
                'class': 'form-control',
                'data-toggle': 'tooltip',
                'data-html': 'true',
                'data-placement': 'right',
                'title': 'Selecciona el ciclo correspondiente a este año lectivo, este se divide en Número de ciclo (1 o 2) y Año calendario.'
                })

    def clean(self, *args, **kwargs):
        cleaned_data = super(EstudioUniversitarioForm, self).clean(*args, **kwargs)
        porc_carrerar_aprob = cleaned_data.get('porc_carrerar_aprob', None)
        if porc_carrerar_aprob is not None:
            if porc_carrerar_aprob < 60:
                self.add_error('porc_carrerar_aprob', 'Aun no esta apto para realizar el servicio social.')


#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


class SolicitudForm(forms.ModelForm):
    codigo_entidad = forms.ModelChoiceField(queryset=EntidadExterna.objects.all().order_by('nombre_entidad'))
    carnet_estudiante = forms.ModelChoiceField(queryset=Estudiante.objects.all().order_by('carnet_estudiante'))

    class Meta:
        model = Solicitud
        widgets = {
            'horas_semana': forms.TextInput(attrs={'placeholder': 'Horas a la Semana', 'autofocus': '', 'required': '', 'maxlength':'3', 'pattern': '([0-9]{1,3})', 'title': 'Ingrese el Total de Horas que realizara a la semana.'}),
            'dias_semana': forms.TextInput(attrs={'placeholder': 'Días a la Semana', 'autofocus': '', 'required': '',  'maxlength':'1', 'pattern': '([0-9]{1})', 'title': 'Ingrese el Total de Días que realizara a la semana.'}),
            'modalidad': forms.TextInput(attrs={'placeholder': 'Modalidad del Servicio', 'autofocus': '', 'required': '', 'maxlength':'30', 'pattern': '([a-zA-Záéíóú ]{3,30})', 'title': 'Ingrese la Modalidad en que desea realizar el Servicio Social.'}),
            'fecha_inicio': forms.TextInput(attrs={'placeholder': 'Fecha de Inicio', 'autocomplete': 'off', 'type':'date', 'min':'1940-01-01'}),
            'fecha_fin': forms.TextInput(attrs={'placeholder': 'Fecha de Finalización', 'autocomplete': 'off', 'type':'date', 'min':'1940-01-01', 'required':'false'}),
        }
        fields = {
            'carnet_estudiante': forms.CharField,
            'codigo_entidad': forms.CharField,
            'horas_semana': forms.CharField,
            'dias_semana': forms.CharField,
            'modalidad': forms.IntegerField,
            'fecha_inicio': forms.DateField,
            'fecha_fin': forms.DateField,
        }
        labels = {
            'carnet_estudiante': 'Carnet Estudiante',
            'codigo_entidad': 'Nombre de la Entidad',
            'horas_semana': 'Horas a la Semana',
            'dias_semana': 'Días a la Semana',
            'modalidad': 'Modalidad del Servicio',
            'fecha_inicio': 'Fecha de Inicio',
            'fecha_fin': 'Fecha Finalización',
        }

    def __init__(self, *args, **kwargs):
        super(SolicitudForm, self).__init__(*args, **kwargs)
        
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'material-control tooltips-general'
                })
        
        self.fields['carnet_estudiante'].widget.attrs.update({
                'class': 'form-control',
                'data-toggle': 'tooltip',
                'data-html': 'true',
                'data-placement': 'right',
                'title': 'Busca tu carnet en la siguiente lista, estos están ordenados en forma ascendente para una búsqueda más rápida. Por favor verifica que hayas seleccionado tu carnet correctamente.'
                })
        self.fields['codigo_entidad'].widget.attrs.update({
                'class': 'form-control',
                'data-toggle': 'tooltip',
                'data-html': 'true',
                'data-placement': 'right',
                'title': 'Selecciona la entidad en la que deseas realizar tu servicio social. Si no encuentras la que deseas puedes sugerir una presionando el botón.'
                })


#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


class EstadoSolicitudForm(forms.ModelForm):
    carnet_estudiante = forms.ModelChoiceField(queryset=Solicitud.objects.all().order_by('carnet_estudiante'))

    class Meta:
        model = EstadoSolicitud
        widgets = {
            'aceptado': forms.Select(choices=estado),
            'motivo': forms.TextInput(attrs={'placeholder': 'Motivo', 'autofocus': '', 'required': False}),
            'observaciones': forms.TextInput(attrs={'placeholder': 'Observaciones', 'autofocus': '', 'required': False}),
        }
        fields = {
            'carnet_estudiante': forms.CharField,
            'aceptado': forms.CharField,
            'motivo': forms.CharField,
            'observaciones': forms.CharField,
        }
        labels = {
            'carnet_estudiante': 'Carnet Estudiante',
            'aceptado': 'Estado de la Solicitud',
            'motivo': 'Motivo',
            'observaciones': 'Observaciones',
        }

    def __init__(self, *args, **kwargs):
        super(EstadoSolicitudForm, self).__init__(*args, **kwargs)
        
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'material-control tooltips-general'
                })
        
        self.fields['carnet_estudiante'].widget.attrs.update({
                'class': 'form-control',
                'data-toggle': 'tooltip',
                'data-html': 'true',
                'data-placement': 'right',
                'title': 'Busca el carnet del estudiante en la siguiente lista, estos están ordenados en forma ascendente para una búsqueda más rápida. Por favor verificar que se haya seleccionado el carnet correcto.'
                })

        self.fields['aceptado'].widget.attrs.update({
                'class': 'form-control',
                })

   

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


