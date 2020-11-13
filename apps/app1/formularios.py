from django.db import transaction
from django.shortcuts import render
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from django.core import serializers
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.views.generic import ListView
from reportlab.platypus import SimpleDocTemplate, Paragraph, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from django.conf import settings
from io import BytesIO
from .models import *
from .forms import *
import time
import os

class generarF1(ListView):
    model = Estudiante
    template_name = 'app1/Estudiante.html'
    context_object_name = 'estudiante'
    success_url = reverse_lazy('proyeccionsocial:generar_F1')  
     
    def cabecera(self,pdf):
        #Utilizamos el archivo logo_django.png que está guardado en la carpeta media/imagenes
        archivo_imagen1 = settings.BASE_DIR+'/static/img/logoUPSAgro.png'
        archivo_imagen2 = settings.BASE_DIR+'/static/img/logoUES.jpg'

        #Definimos el tamaño de la imagen a cargar y las coordenadas correspondientes
        pdf.drawImage(archivo_imagen1, 50, 730, 125, 90,preserveAspectRatio=True) 
        pdf.drawImage(archivo_imagen2, 430, 720, 125, 90,preserveAspectRatio=True) 

        # Establecemos el tamaño de letra en 8 y el tipo de letra Helvetica en negrita
        # Luego en drawString se colocan las coordenadas X Y de donde se quiere poner
        # el texto, el eje Y inicia en la parte inferior izquierda, ahi es el punto (0, 0)
        pdf.setFont("Helvetica-Bold", 8)
        pdf.drawString(248, 780, u"UNIVERSIDAD DE EL SALVADOR")

        pdf.setFont("Helvetica-Bold", 8)
        pdf.drawString(232, 770, u"FACULTAD DE CIENCIAS AGRONOMICAS")  

        pdf.setFont("Helvetica-Bold", 8)
        pdf.drawString(234, 760, u"UNIDAD DE DESARROLLO ACADEMICO") 

        pdf.setFont("Helvetica-Bold", 8)
        pdf.drawString(245, 750, u"UNIDAD DE PROYECCION SOCIAL")       

    def get_queryset(self, pdf, **kwargs):
        carnet_estudiante = self.kwargs.get('carnet_estudiante')
        queryset = Estudiante.objects.filter(carnet_estudiante = carnet_estudiante)

        for i in Estudiante.objects.filter(carnet_estudiante = carnet_estudiante):
            carnet = i.carnet_estudiante
            nombre = i.nombre_estudiante
            apellido = i.apellido_estudiante
            sexo = i.sexo_estudiante
            telefono = i.telefono_estudiante
            correo = i.correo_estudiante
            direccion = i.direccion_estudiante

        j=0

        for i in Estudiante.objects.all():
            carnetBusqueda = i.carnet_estudiante
            if carnetBusqueda == carnet:
                posicion = j + 1
            else:
                j = j + 1

        numero = posicion

        for i in EstudioUniversitario.objects.filter(carnet_estudiante = carnet_estudiante):
            carrera = i.codigo_carrera.nombre_carrera
            porc_carrera = i.porc_carrerar_aprob
            und_valor = i.unidades_valorativas
            experiencia = i.experiencia_areas_conoc
            ciclo_lect = i.codigo_ciclo

        for i in Solicitud.objects.filter(carnet_estudiante = carnet_estudiante):
            horas_sem = i.horas_semana
            dias_sem = i.dias_semana
            entidad = i.codigo_entidad
            modalidad = i.modalidad
            fecha_inicio = i.fecha_inicio

        aceptado = "** ¡NO ASIGNADO AÚN! **"
        motivo = "** ¡NO ASIGNADO AÚN! **"
        observaciones = "** ¡NO ASIGNADO AÚN! **"

        for i in EstadoSolicitud.objects.filter(carnet_estudiante = carnet_estudiante): 
            aceptado = i.aceptado

            if i.motivo == None:
                motivo = " - "
            else:
                motivo = i.motivo

            if i.observaciones == None:
                observaciones = " - "
            else:
                observaciones = i.observaciones

        texto = 'No. Correlativo: %s' % numero
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(450, 705, texto)

        pdf.setFont("Helvetica-Bold", 26)
        pdf.drawString(100, 720, u"F-1")

        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(235, 710, u"SOLICITUD DE SERVICIO SOCIAL")

        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(60, 690, u"DATOS PERSONALES")

        texto = 'Nombre Completo: %s' % nombre +' '+ apellido
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 675, texto)

        #--------------------------------------
        #texto = 'Nombre Completo: ' 
        #pdf.setFont("Helvetica-Bold", 10)
        #pdf.drawString(60, 675, texto)

        #texto = ' %s' % nombre
        #pdf.setFont("Helvetica", 10)
        #pdf.drawString(150, 675, texto)
        #---------------------------------------

        texto = 'Sexo: %s' % sexo
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 660, texto)

        texto = 'Telefono: %s' % telefono
        pdf.setFont("Helvetica", 10)
        pdf.drawString(150, 660, texto)

        texto = 'Correo: %s' % correo
        pdf.setFont("Helvetica", 10)
        pdf.drawString(330, 660, texto)

        texto = 'Direccion Residencial: %s' % direccion
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 645, texto)

        #Agrega una linea horizontal como division
        pdf.line(60, 630, 560, 630)

        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(60, 610, u"ESTUDIO UNIVERSITARIO")

        texto = 'Carrera: %s' % carrera
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 595, texto)

        texto = 'Carnet No.: %s' % carnet
        pdf.setFont("Helvetica", 10)
        pdf.drawString(450, 595, texto)

        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(60, 575, u"Estado Academico:")

        texto = 'Porcentaje de la carrera aprobado: %s' % porc_carrera
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 560, texto)

        texto = 'Unidades Valorativas: %s' % und_valor
        pdf.setFont("Helvetica", 10)
        pdf.drawString(280, 560, texto)

        texto = 'Ciclo Lectivo: %s' % ciclo_lect
        pdf.setFont("Helvetica", 10)
        pdf.drawString(450, 560, texto)

        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 545, u"Experiencia en algunas areas de conocimiento de su carrera: ")

        texto = '%s' % experiencia
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 530, texto)

        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(60, 495, u"Tiempo disponible para su desarrollo social: ")

        texto = 'Horas por Semana: %s' % horas_sem
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 480, texto)

        texto = 'Dias por Semana: %s' % dias_sem
        pdf.setFont("Helvetica", 10)
        pdf.drawString(330, 480, texto)

        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 465, u"Propuesta de la entidad donde realizara su servicio social segun el ambito mencionado en el Manual de ")
        pdf.drawString(60, 450, u"procedimientos del Servicio Social: ")

        texto = '%s' % entidad
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 435, texto)

        #Agrega una linea horizontal como division
        pdf.line(60, 420, 560, 420)

        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 400, u"Propuesta de modalidad de servicio segun las mencionadas en el Manual de Procedimientos del Servicio ")

        texto = 'Social: %s' % modalidad
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 385, texto)

        texto = 'Fecha de Inicio posible: %s' % fecha_inicio
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 370, texto)

        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 335, u"Firma del solicitante: ")
        pdf.line(155, 335, 300, 335)

        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 305, u"Ciudad Universitaria, ")
        pdf.line(155, 305, 200, 305)

        pdf.setFont("Helvetica", 10)
        pdf.drawString(210, 305, u"de")
        pdf.line(230, 305, 320, 305)

        pdf.setFont("Helvetica", 10)
        pdf.drawString(330, 305, u"del ")
        pdf.line(350, 305, 410, 305)

        #Agrega una linea horizontal como division
        pdf.line(60, 285, 560, 285)

        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(60, 265, u"PARA USO EXCLUSIVO DE PROYECCION SOCIAL ")

        if aceptado == "** ¡NO ASIGNADO AÚN! **":
            texto = 'Aceptado: %s' % aceptado
            pdf.setFont("Helvetica-Bold", 10)
            pdf.drawString(60, 245, texto)

            texto = 'Motivo: %s' % motivo
            pdf.setFont("Helvetica-Bold", 10)
            pdf.drawString(265, 245, texto)

            pdf.setFont("Helvetica-Bold", 10)
            pdf.drawString(60, 225, u"Observaciones: ")

            texto = '%s' % observaciones
            pdf.setFont("Helvetica-Bold", 10)
            pdf.drawString(60, 210, texto)
        else:
            texto = 'Aceptado: %s' % aceptado
            pdf.setFont("Helvetica", 10)
            pdf.drawString(60, 245, texto)

            texto = 'Motivo: %s' % motivo
            pdf.setFont("Helvetica", 10)
            pdf.drawString(200, 245, texto)

            pdf.setFont("Helvetica", 10)
            pdf.drawString(60, 225, u"Observaciones: ")

            texto = '%s' % observaciones
            pdf.setFont("Helvetica", 10)
            pdf.drawString(60, 210, texto)

        return queryset

    def get_context_data(self, **kwargs):
        context = super(generarF1, self).get_context_data(**kwargs)
        carnet_estudiante = self.kwargs.get('carnet_estudiante')
        context['carnet_estudiante'] = carnet_estudiante
        return context
         
    def get(self, request, *args, **kwargs):
        #Indicamos el tipo de contenido a devolver, en este caso un pdf
        response = HttpResponse(content_type='application/pdf')

        pdf_name = "Comprobante_F1_UPS.pdf"
        # Esta linea es por si deseas descargar el pdf a tu computadora
        response['Content-Disposition'] = 'inline; filename=%s' % pdf_name

        #La clase io.BytesIO permite tratar un array de bytes como un fichero binario, se utiliza como almacenamiento temporal
        buffer = BytesIO()

        #Canvas nos permite hacer el reporte con coordenadas X y Y
        pdf = canvas.Canvas(buffer)

        #Llamo al método cabecera donde están definidos los datos que aparecen en la cabecera del reporte.
        self.cabecera(pdf)
        self.get_queryset(pdf)

        #Con show page hacemos un corte de página para pasar a la siguiente
        pdf.showPage()
        pdf.save()
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response


# #-----------------------------------------------------------------------------------------------


class generarF2(ListView):
    model = Estudiante
    template_name = 'app1/Estudiante.html'
    context_object_name = 'estudiante'
    success_url = reverse_lazy('proyeccionsocial:generar_F2')  
     
    def cabecera(self,pdf):
         #Utilizamos el archivo logo_django.png que está guardado en la carpeta media/imagenes
        archivo_imagen1 = settings.BASE_DIR+'/static/img/logoUPSAgro.png'
        archivo_imagen2 = settings.BASE_DIR+'/static/img/logoUES.jpg'

        #Definimos el tamaño de la imagen a cargar y las coordenadas correspondientes
        pdf.drawImage(archivo_imagen1, 50, 730, 125, 90,preserveAspectRatio=True) 
        pdf.drawImage(archivo_imagen2, 430, 720, 125, 90,preserveAspectRatio=True) 

        # Establecemos el tamaño de letra en 8 y el tipo de letra Helvetica en negrita
        # Luego en drawString se colocan las coordenadas X Y de donde se quiere poner
        # el texto, el eje Y inicia en la parte inferior izquierda, ahi es el punto (0, 0)
        pdf.setFont("Helvetica-Bold", 8)
        pdf.drawString(248, 780, u"UNIVERSIDAD DE EL SALVADOR")

        pdf.setFont("Helvetica-Bold", 8)
        pdf.drawString(232, 770, u"FACULTAD DE CIENCIAS AGRONOMICAS")  

        pdf.setFont("Helvetica-Bold", 8)
        pdf.drawString(234, 760, u"UNIDAD DE DESARROLLO ACADEMICO") 

        pdf.setFont("Helvetica-Bold", 8)
        pdf.drawString(245, 750, u"UNIDAD DE PROYECCION SOCIAL")       

    def get_queryset(self, pdf, **kwargs):
        carnet_estudiante = self.kwargs.get('carnet_estudiante')
        queryset = Estudiante.objects.filter(carnet_estudiante = carnet_estudiante)

        for i in Estudiante.objects.filter(carnet_estudiante = carnet_estudiante):
            carnet = i.carnet_estudiante
            nombre = i.nombre_estudiante
            apellido = i.apellido_estudiante

        for i in EstudioUniversitario.objects.filter(carnet_estudiante = carnet_estudiante):
            carrera = i.codigo_carrera.nombre_carrera
            ciclo_lect = i.codigo_ciclo

        for i in Solicitud.objects.filter(carnet_estudiante = carnet_estudiante):
            horas_sem = i.horas_semana
            dias_sem = i.dias_semana
            entidad = i.codigo_entidad
            modalidad = i.modalidad
            fecha_inicio = i.fecha_inicio
            fecha_fin = i.fecha_fin

        aceptado = "NO"
        motivo = "Debe escoger otra entidad."
        observaciones = "Porfavor escoja otra entidad para poder realizar su servicio social."

        pdf.setFont("Helvetica-Bold", 26)
        pdf.drawString(100, 720, u"F2")

        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(180, 710, u"CARTA DE ASIGNACIÓN DEL SERVICIO SOCIAL")

        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 690, u"El/La suscrito (a), Jefe(a) de la Unidad de Proyección Social de la Facultad de Ciencias Agronómicas,")

        pdf.drawString(60, 675, u"hace constar que el (la)")

        texto = 'Bachiller %s' % nombre
        pdf.drawString(60, 660, texto)

        texto = 'Carné No. %s       matriculado (a) en la carrera de:' % carnet
        pdf.drawString(60, 645, texto)

        texto = carrera
        pdf.drawString(60, 630, texto)

        pdf.line(60, 616, 545, 616)
        pdf.line(60, 617, 545, 617)

        pdf.drawString(60, 600, u'se le ha aceptado el servicio social para la realizarlo en (la entidad):')

        texto = entidad.__str__()
        pdf.drawString(60, 585, texto)

        data = [['Modalidad de servicio social','Lugar de ejecución','Período de ejecución','','No. horas semanales'],
                ['','', 'inicial','final',''],
                [modalidad, entidad.__str__(), fecha_inicio.__str__(), fecha_fin.__str__(), horas_sem.__str__()]]
        style = getSampleStyleSheet()
        dataParrafos = [[Paragraph(cell, style["Normal"]) for cell in row] for row in data]
        t = Table(dataParrafos,colWidths=[130,130,70,70,80],rowHeights=[25,25,100])
        t.setStyle(TableStyle([('GRID',(0,0),(-1,-1),0.5,colors.black),
                               ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                               ('SPAN',(0,0),(0,1)),
                               ('SPAN',(1,0),(1,1)),
                               ('SPAN',(4,0),(4,1)),
                               ('SPAN',(2,0),(3,0))]))
        t.wrapOn(pdf,560,590)
        t.drawOn(pdf,60,420)

        texto = 'Asesor por parte de la entidad externa: %s' % 'Asesor'
        pdf.drawString(60, 400,texto)

        texto = 'Asesor por parte de la Facultad: %s' % 'Asesor'
        pdf.drawString(60, 370, texto)

        pdf.drawString(60, 340, u"Y para los tramites de presentación en la institución o comunidad se extiende la presente")

        pdf.drawString(60, 305, u"Ciudad Universitaria a los ")
        pdf.line(175, 305, 210, 305)

        pdf.drawString(210, 305, u"días del mes de")
        pdf.line(280, 305, 358, 305)

        pdf.drawString(360, 305, u"del año")
        pdf.line(400, 305, 430, 305)

        pdf.drawString(200, 265, u'"HACIA LA LIBERTAD POR LA CULTURA"')

        pdf.drawString(60, 150, u'Firma y sello')
        pdf.line(130,150,450,150)

         #Utilizamos el archivo logo_django.png que está guardado en la carpeta media/imagenes
        archivo_imagen1 = settings.BASE_DIR+'/static/img/firmaYSello.jpg'

        #Definimos el tamaño de la imagen a cargar y las coordenadas correspondientes
        pdf.drawImage(archivo_imagen1, 60, 151, 460, 95,preserveAspectRatio=True) 
        # 60 es el ancho de la imagen, 151 es el alto en posicion, 450 es el tamaño del borde izq., 60 es lo alto en diagonal de la imagen

        pdf.drawString(195, 135, u'Jefe(a) de la Unidad de Proyección Social')

        return queryset

    def get_context_data(self, **kwargs):
        context = super(generarF2, self).get_context_data(**kwargs)
        carnet_estudiante = self.kwargs.get('carnet_estudiante')
        context['carnet_estudiante'] = carnet_estudiante
        return context
         
    def get(self, request, *args, **kwargs):
        #Indicamos el tipo de contenido a devolver, en este caso un pdf
        response = HttpResponse(content_type='application/pdf')

        pdf_name = "Comprobante_F2_UPS.pdf"
        # Esta linea es por si deseas descargar el pdf a tu computadora
        response['Content-Disposition'] = 'inline; filename=%s' % pdf_name

        #La clase io.BytesIO permite tratar un array de bytes como un fichero binario, se utiliza como almacenamiento temporal
        buffer = BytesIO()

        #Canvas nos permite hacer el reporte con coordenadas X y Y
        pdf = canvas.Canvas(buffer)

        #Llamo al método cabecera donde están definidos los datos que aparecen en la cabecera del reporte.
        self.cabecera(pdf)
        self.get_queryset(pdf)

        #Con show page hacemos un corte de página para pasar a la siguiente
        pdf.showPage()
        pdf.save()
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response

# #-----------------------------------------------------------------------------------------------


class generarF3(ListView):
    model = Estudiante
    template_name = 'app1/Estudiante.html'
    context_object_name = 'estudiante'
    success_url = reverse_lazy('proyeccionsocial:generar_F3')  
     
    def cabecera(self,pdf):
         #Utilizamos el archivo logo_django.png que está guardado en la carpeta media/imagenes
        archivo_imagen1 = settings.BASE_DIR+'/static/img/logoUPSAgro.png'
        archivo_imagen2 = settings.BASE_DIR+'/static/img/logoUES.jpg'

        #Definimos el tamaño de la imagen a cargar y las coordenadas correspondientes
        pdf.drawImage(archivo_imagen1, 50, 730, 125, 90,preserveAspectRatio=True) 
        pdf.drawImage(archivo_imagen2, 430, 720, 125, 90,preserveAspectRatio=True) 

        # Establecemos el tamaño de letra en 8 y el tipo de letra Helvetica en negrita
        # Luego en drawString se colocan las coordenadas X Y de donde se quiere poner
        # el texto, el eje Y inicia en la parte inferior izquierda, ahi es el punto (0, 0)
        pdf.setFont("Helvetica-Bold", 8)
        pdf.drawString(248, 780, u"UNIVERSIDAD DE EL SALVADOR")

        pdf.setFont("Helvetica-Bold", 8)
        pdf.drawString(232, 770, u"FACULTAD DE CIENCIAS AGRONOMICAS")  

        pdf.setFont("Helvetica-Bold", 8)
        pdf.drawString(234, 760, u"UNIDAD DE DESARROLLO ACADEMICO") 

        pdf.setFont("Helvetica-Bold", 8)
        pdf.drawString(245, 750, u"UNIDAD DE PROYECCION SOCIAL")     

    def get_queryset(self, pdf, **kwargs):
        carnet_estudiante = self.kwargs.get('carnet_estudiante')
        queryset = Estudiante.objects.filter(carnet_estudiante = carnet_estudiante)
        #Declaracion y asignacion de variables que se recuperaran de la BD

        nombre = "Karla María Abrego Reyes"
        numero_control = "2"
        domicilio= "Urb. Valle del Quetzal, pje El Nogal "
        tel = "78680257"
        correo = "ar14019@ues.edu.sv"
        carrera = "Ingeniería de Sistemas Informáticos"
        ciclo = "Impar"
        entidad = "I"
        domicilio_entidad ="L"
        fecha_inicio = "12/10/20"
        fecha_final = "12/10/21"
        
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(180, 710, u"CARTA DE COMPROMISO DEL SERVICIO SOCIAL")

        pdf.setFont("Helvetica-Bold", 26)
        pdf.drawString(100, 715, u"F3")

        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 690, u"Con el fin de dar cumplimiento a lo establecido en el Manual de Procedimientos del Servicio Social")
        pdf.drawString(60, 675, u"de la Facultad de Ciencias Agronómicas de la Universidad de El Salvador, el suscrito:")

        texto = 'NOMBRE:  %s' % nombre
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 652, texto)

        texto = 'No. DE CONTROL:  %s' % numero_control
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 637, texto)

        texto = 'DOMICILIO:  %s' % domicilio
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 602, texto)

        texto = 'TEL:  %s' % tel
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 584, texto)

        texto = 'CORRREO ELECTRONICO:  %s' % correo
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 569, texto)

        texto = 'CARRERA:  %s' % carrera
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 534, texto)

        texto = 'CICLO:  %s' % ciclo
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 519, texto)

        texto = 'ENTIDAD:  %s' % entidad
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 484, texto)

        texto = 'DOMICILIO DE LA ENTIDAD:  %s' % domicilio_entidad
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 469, texto)

        texto = 'FECHA DE INICIO:  %s' % fecha_inicio
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 429, texto)

        texto = 'FECHA DE FINALIZACION:  %s' % fecha_final
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 414, texto)

        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 379, u"Me comprometo a realizar el Servicio Social acatando el Reglamento General de Proyección Social")

        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 364, u"de la Universidad de El Salvador y llevarlo  a cabo en lugar y periodos manifestados,así como, a ")
        
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 349, u"participar con mis conocimientos e iniciativa en las actividades que desempeñe, procurando dar")
        
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 334, u"una imagen positiva de la Institución de la entidad, de no serlo así, quedo enterado(a) de la")    

        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 319, u"cancelación respectiva, la cual procederá automáticamente")
    
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 284, u"En la ciudad de:")
        pdf.line(136, 284, 200, 284)

        pdf.setFont("Helvetica", 10)
        pdf.drawString(200, 284, u"del día")
        pdf.line(235, 284, 328, 284)

        pdf.setFont("Helvetica", 10)
        pdf.drawString(335, 284, u"del mes")
        pdf.line(375, 284, 450, 284)

        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 269, u"de")
        pdf.line(85, 269, 160, 269)

        pdf.line(240, 200, 340, 200) #linea de la firma

        pdf.setFont("Helvetica", 10)
        pdf.drawString(244, 185, u"Firma del estudiante")

        return queryset
 
    def get_context_data(self, **kwargs):
        context = super(generarF3, self).get_context_data(**kwargs)
        carnet_estudiante = self.kwargs.get('carnet_estudiante')
        context['carnet_estudiante'] = carnet_estudiante
        return context
         
    def get(self, request, *args, **kwargs):
        #Indicamos el tipo de contenido a devolver, en este caso un pdf
        response = HttpResponse(content_type='application/pdf')

        pdf_name = "Comprobante_F3_UPS.pdf"
        # Esta linea es por si deseas descargar el pdf a tu computadora
        response['Content-Disposition'] = 'inline; filename=%s' % pdf_name

        #La clase io.BytesIO permite tratar un array de bytes como un fichero binario, se utiliza como almacenamiento temporal
        buffer = BytesIO()

        #Canvas nos permite hacer el reporte con coordenadas X y Y
        pdf = canvas.Canvas(buffer)

        #Llamo al método cabecera donde están definidos los datos que aparecen en la cabecera del reporte.
        self.cabecera(pdf)
        self.get_queryset(pdf)

        #Con show page hacemos un corte de página para pasar a la siguiente
        pdf.showPage()
        pdf.save()
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response


# #-----------------------------------------------------------------------------------------------


class generarF4TI(ListView):
    model = Estudiante
    template_name = 'app1/Estudiante.html'
    context_object_name = 'estudiante'
    success_url = reverse_lazy('proyeccionsocial:generar_F4TI')  
     
    def cabecera(self,pdf):
         #Utilizamos el archivo logo_django.png que está guardado en la carpeta media/imagenes
        archivo_imagen1 = settings.BASE_DIR+'/static/img/logoUPSAgro.png'
        archivo_imagen2 = settings.BASE_DIR+'/static/img/logoUES.jpg'

        #Definimos el tamaño de la imagen a cargar y las coordenadas correspondientes
        pdf.drawImage(archivo_imagen1, 50, 730, 125, 90,preserveAspectRatio=True) 
        pdf.drawImage(archivo_imagen2, 430, 720, 125, 90,preserveAspectRatio=True) 

        # Establecemos el tamaño de letra en 8 y el tipo de letra Helvetica en negrita
        # Luego en drawString se colocan las coordenadas X Y de donde se quiere poner
        # el texto, el eje Y inicia en la parte inferior izquierda, ahi es el punto (0, 0)
        pdf.setFont("Helvetica-Bold", 8)
        pdf.drawString(248, 780, u"UNIVERSIDAD DE EL SALVADOR")

        pdf.setFont("Helvetica-Bold", 8)
        pdf.drawString(232, 770, u"FACULTAD DE CIENCIAS AGRONOMICAS")  

        pdf.setFont("Helvetica-Bold", 8)
        pdf.drawString(234, 760, u"UNIDAD DE DESARROLLO ACADEMICO") 

        pdf.setFont("Helvetica-Bold", 8)
        pdf.drawString(245, 750, u"UNIDAD DE PROYECCION SOCIAL")     

    def get_queryset(self, pdf, **kwargs):
        carnet_estudiante = self.kwargs.get('carnet_estudiante')
        queryset = Estudiante.objects.filter(carnet_estudiante = carnet_estudiante)
        #Declaracion y asignacion de variables que se recuperaran de la BD

        tutor="(nombre completo del TUTOR)"
        alumno="(nombre completo del ALUMNO)"
        proyecto="(nombre del PROYECTO)"
        departamento="(nombre del DEPARTAMENTO)"
        superior="(nombre del INGENIERO o LICENCIADO)"
        fecha="(00/00/00)"
        externo="(nombre completo del TUTOR EXTERNO)"
        entidad="(nombre completo de la ENTIDAD o COMUNIDAD)"

        pdf.setFont("Helvetica-Bold", 26)
        pdf.drawString(100, 720, u"F4-TI")

        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(90, 700, u"NOMBRAMIENTO DEL TUTOR INTERNO PARA LA EJECUCION DEL SERVICIO SOCIAL")

        texto = "Por este medio se nombra a: "
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 675, texto)
        
        texto = '%s' % tutor
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 660, texto)

        texto = "como tutor interno en la ejecución del Servicio Social que desarrollará el (la) bachiller: "
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 645, texto)

        texto = '%s ' %alumno
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 630, texto)
        
        texto = 'en el proyecto denominado: ' 
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 615, texto)
        
        texto = '%s ' %proyecto
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 600, texto)
        
        texto = "a propuesta del jefe del Departamento de: "
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 565, texto)
        
        texto = '%s ' %departamento
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 550, texto)
        
        texto = "Ing. (Lic.): " 
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 535, texto)
        
        texto = '%s ' %superior
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 520, texto)
        
        texto = "El proyecto se iniciará a partir de esta fecha (dd/mm/aa): " 
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 505, texto)
        
        texto = '%s ' %fecha
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 490, texto)
        
        texto = "El tutor externo será: " 
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 475, texto)
        
        texto = '%s ' %externo
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 460, texto)
        
        texto = "representando a la entidad o comunidad: " 
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 445, texto)
        
        texto = '%s ' %entidad
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 430, texto)
        
        texto = "Todo esto, de acuerdo a las cláusulas del Manual de Procedimientos para la ejecución del Servicio Social" 
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 400, texto)
        
        texto = "de la Facultad y al Reglamento respectivo, por lo que se solicita velar por el fiel cumplimiento del" 
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 385, texto)
        
        texto = "trabajo antes mencionado." 
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 370, texto)
        
        texto = "Firma y sello: _______________________________" 
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 300, texto)
        
        texto = "Fecha:_________________ de _________________ de _________________" 
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 250, texto)

        return queryset
 
    def get_context_data(self, **kwargs):
        context = super(generarF4TI, self).get_context_data(**kwargs)
        carnet_estudiante = self.kwargs.get('carnet_estudiante')
        context['carnet_estudiante'] = carnet_estudiante
        return context
         
    def get(self, request, *args, **kwargs):
        #Indicamos el tipo de contenido a devolver, en este caso un pdf
        response = HttpResponse(content_type='application/pdf')

        pdf_name = "Comprobante_F4-TI_UPS.pdf"
        # Esta linea es por si deseas descargar el pdf a tu computadora
        response['Content-Disposition'] = 'inline; filename=%s' % pdf_name

        #La clase io.BytesIO permite tratar un array de bytes como un fichero binario, se utiliza como almacenamiento temporal
        buffer = BytesIO()

        #Canvas nos permite hacer el reporte con coordenadas X y Y
        pdf = canvas.Canvas(buffer)

        #Llamo al método cabecera donde están definidos los datos que aparecen en la cabecera del reporte.
        self.cabecera(pdf)
        self.get_queryset(pdf)

        #Con show page hacemos un corte de página para pasar a la siguiente
        pdf.showPage()
        pdf.save()
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response


# #-----------------------------------------------------------------------------------------------


class generarF4TE(ListView):
    model = Estudiante
    template_name = 'app1/Estudiante.html'
    context_object_name = 'estudiante'
    success_url = reverse_lazy('proyeccionsocial:generar_F4TE')  
     
    def cabecera(self,pdf):
         #Utilizamos el archivo logo_django.png que está guardado en la carpeta media/imagenes
        archivo_imagen1 = settings.BASE_DIR+'/static/img/logoUPSAgro.png'
        archivo_imagen2 = settings.BASE_DIR+'/static/img/logoUES.jpg'

        #Definimos el tamaño de la imagen a cargar y las coordenadas correspondientes
        pdf.drawImage(archivo_imagen1, 50, 730, 125, 90,preserveAspectRatio=True) 
        pdf.drawImage(archivo_imagen2, 430, 720, 125, 90,preserveAspectRatio=True) 

        # Establecemos el tamaño de letra en 8 y el tipo de letra Helvetica en negrita
        # Luego en drawString se colocan las coordenadas X Y de donde se quiere poner
        # el texto, el eje Y inicia en la parte inferior izquierda, ahi es el punto (0, 0)
        pdf.setFont("Helvetica-Bold", 8)
        pdf.drawString(248, 780, u"UNIVERSIDAD DE EL SALVADOR")

        pdf.setFont("Helvetica-Bold", 8)
        pdf.drawString(232, 770, u"FACULTAD DE CIENCIAS AGRONOMICAS")  

        pdf.setFont("Helvetica-Bold", 8)
        pdf.drawString(234, 760, u"UNIDAD DE DESARROLLO ACADEMICO") 

        pdf.setFont("Helvetica-Bold", 8)
        pdf.drawString(245, 750, u"UNIDAD DE PROYECCION SOCIAL")     

    def get_queryset(self, pdf, **kwargs):
        carnet_estudiante = self.kwargs.get('carnet_estudiante')
        queryset = Estudiante.objects.filter(carnet_estudiante = carnet_estudiante)
        #Declaracion y asignacion de variables que se recuperaran de la BD

        entidad="(nombre de la ENTIDAD)"
        externo="(nombre del TUTOR EXTERNO)"
        alumno="(nombre del ALUMNO)"
        proyecto="(nombre del PROYECTO)"
        fecha="(00/00/00)"
        dia = "(00)"
        mes = "(mes)"
        anio= "(0000)"
        y=720

        pdf.setFont("Helvetica-Bold", 26)
        pdf.drawString(100, 720, u"F4-TE")
        
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(90, 700, u"DESIGNACIÓN DEL TUTOR EXTERNO PARA LA EJECUCIÓN DEL SERVICIO SOCIAL")
        
        texto = "La %s " %entidad
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 675, texto)
        
        texto = "Por este medio designa a: %s" %externo
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 645, texto)
        
        texto = "como tutor externo para la ejecución del Servicio Social que desarrollará el(la) bachiller: " 
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 630, texto)
        
        texto = "%s" %alumno
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 615, texto)
        
        texto = "en el proyecto denominado: " 
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 600, texto)
        
        texto = "%s " %proyecto
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 585, texto)
        
        texto = "El proyecto se iniciará a partir de esta fecha (dd/mm/aa): " 
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 555, texto)
        
        texto = "%s " %fecha
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 540, texto)
 
        texto = "Todo esto, de acuerdo a las cláusulas del Manual de Procedimientos para la ejecución del Servicio Social"
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 500, texto)
        
        texto = "de la Facultad y al Reglamento respectivo, por lo que se solicita velar por el fiel cumplimiento del trabajo"
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 485, texto)
        
        texto = "antes mencionado."
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 470, texto)
        
        
        texto = "Firma y sello de la entidad: "
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 445, texto)
        
        texto = "_______________________________________________________"
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 400, texto)
        
        texto = "Fecha: "+dia+" de "+mes+" de "+ anio
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 350, texto)

        return queryset
 
    def get_context_data(self, **kwargs):
        context = super(generarF4TE, self).get_context_data(**kwargs)
        carnet_estudiante = self.kwargs.get('carnet_estudiante')
        context['carnet_estudiante'] = carnet_estudiante
        return context
         
    def get(self, request, *args, **kwargs):
        #Indicamos el tipo de contenido a devolver, en este caso un pdf
        response = HttpResponse(content_type='application/pdf')

        pdf_name = "Comprobante_F4-TE_UPS.pdf"
        # Esta linea es por si deseas descargar el pdf a tu computadora
        response['Content-Disposition'] = 'inline; filename=%s' % pdf_name

        #La clase io.BytesIO permite tratar un array de bytes como un fichero binario, se utiliza como almacenamiento temporal
        buffer = BytesIO()

        #Canvas nos permite hacer el reporte con coordenadas X y Y
        pdf = canvas.Canvas(buffer)

        #Llamo al método cabecera donde están definidos los datos que aparecen en la cabecera del reporte.
        self.cabecera(pdf)
        self.get_queryset(pdf)

        #Con show page hacemos un corte de página para pasar a la siguiente
        pdf.showPage()
        pdf.save()
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response


# #-----------------------------------------------------------------------------------------------


class generarF6(ListView):
    model = Estudiante
    template_name = 'app1/Estudiante.html'
    context_object_name = 'estudiante'
    success_url = reverse_lazy('proyeccionsocial:generar_F6')  
     
    def cabecera(self,pdf):
         #Utilizamos el archivo logo_django.png que está guardado en la carpeta media/imagenes
        archivo_imagen1 = settings.BASE_DIR+'/static/img/logoUPSAgro.png'
        archivo_imagen2 = settings.BASE_DIR+'/static/img/logoUES.jpg'

        #Definimos el tamaño de la imagen a cargar y las coordenadas correspondientes
        pdf.drawImage(archivo_imagen1, 50, 730, 125, 90,preserveAspectRatio=True) 
        pdf.drawImage(archivo_imagen2, 430, 720, 125, 90,preserveAspectRatio=True) 

        # Establecemos el tamaño de letra en 8 y el tipo de letra Helvetica en negrita
        # Luego en drawString se colocan las coordenadas X Y de donde se quiere poner
        # el texto, el eje Y inicia en la parte inferior izquierda, ahi es el punto (0, 0)
        pdf.setFont("Helvetica-Bold", 8)
        pdf.drawString(248, 780, u"UNIVERSIDAD DE EL SALVADOR")

        pdf.setFont("Helvetica-Bold", 8)
        pdf.drawString(232, 770, u"FACULTAD DE CIENCIAS AGRONOMICAS")  

        pdf.setFont("Helvetica-Bold", 8)
        pdf.drawString(234, 760, u"UNIDAD DE DESARROLLO ACADEMICO") 

        pdf.setFont("Helvetica-Bold", 8)
        pdf.drawString(245, 750, u"UNIDAD DE PROYECCION SOCIAL")     

    def get_queryset(self, pdf, **kwargs):
        carnet_estudiante = self.kwargs.get('carnet_estudiante')
        queryset = Estudiante.objects.filter(carnet_estudiante = carnet_estudiante)
        #Declaracion y asignacion de variables que se recuperaran de la BD

        for i in Estudiante.objects.filter(carnet_estudiante = carnet_estudiante):
            carnet = i.carnet_estudiante
            nombre = i.nombre_estudiante
            apellido = i.apellido_estudiante

        j=0

        for i in Estudiante.objects.all():
            carnetBusqueda = i.carnet_estudiante
            if carnetBusqueda == carnet:
                posicion = j + 1
            else:
                j = j + 1

        numero = posicion

        for i in EstudioUniversitario.objects.filter(carnet_estudiante = carnet_estudiante):
            carrera = i.codigo_carrera.nombre_carrera
            ciclo_lect = i.codigo_ciclo

        for i in Solicitud.objects.filter(carnet_estudiante = carnet_estudiante):
            horas_sem = i.horas_semana
            dias_sem = i.dias_semana
            entidad = i.codigo_entidad
            modalidad = i.modalidad
            fecha_inicio = i.fecha_inicio
            fecha_fin = i.fecha_fin
        
        aceptado = "NO"
        motivo = "Debe escoger otra entidad."
        observaciones = "Porfavor escoja otra entidad para poder realizar su servicio social."

        texto = 'No. Correlativo: %s' % numero
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(450, 707, texto)

        pdf.setFont("Helvetica-Bold", 26)
        pdf.drawString(100, 720, u"F6")

        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(100, 690, u"CONSTANCIA DE APROBACIÓN DEL PLAN DE TRABAJO DEL SERVICIO SOCIAL")

        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 670, u"Los suscritos, tutores del servicio social, hacen constar que el (la)")

        texto = 'Bachiller %s' % nombre
        pdf.drawString(60, 655, texto)

        texto = 'Carné No. %s       matriculado (a) en la carrera:' % carnet
        pdf.drawString(60, 640, texto)

        texto = carrera
        pdf.drawString(70, 625, texto)

        pdf.line(60, 614, 515, 614)
        pdf.line(60, 613, 515, 613)

        pdf.drawString(60, 595, u'ha cumplido satisfactoriamente con todos los requerimientos de elaboración del plan para')
        pdf.drawString(60, 580, u'desarrollar su servicio social conforme a la descripción que se detalla a continuación:')

        data = [
            ['Modalidad de servicio social', 'Entidad y Lugar de ejecución', 'Período de ejecución', '', 'Actividades generales del plan', 'Fuente de Financiami-ento' ,'No. horas semanales'],
            ['', '', 'inicial', 'final', ''],
            [modalidad, entidad.__str__(), fecha_inicio.__str__(), fecha_fin.__str__(),'', '', horas_sem.__str__()]]

        style = getSampleStyleSheet()
        dataParrafos = [[Paragraph(cell, style["Normal"]) for cell in row] for row in data]
        t = Table(dataParrafos, colWidths=[65,65,40,40,95,65,65], rowHeights=[30,30,100])
        t.setStyle(TableStyle([('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                               ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                               ('SPAN', (0, 0), (0, 1)),
                               ('SPAN', (1, 0), (1, 1)),
                               ('SPAN', (4, 0), (4, 1)),
                               ('SPAN', (5, 0), (5, 1)),
                               ('SPAN', (6, 0), (6, 1)),
                               ('SPAN', (2, 0), (3, 0))]))
        t.wrapOn(pdf, 560, 590)
        t.drawOn(pdf, 60, 400)

        pdf.drawString(200, 360, u'"HACIA LA LIBERTAD POR LA CULTURA"')

        texto = 'Nombre y firma de tutor interno: %s' % 'Asesor'
        pdf.drawString(60, 320, texto)
        pdf.line(205, 318, 450, 318)

        texto = 'Nombre y firma de tutor externo: %s' % 'Asesor'
        pdf.drawString(60, 280, texto)
        pdf.line(205,278,450,278)

        pdf.drawString(60, 200, u"Ciudad Universitaria a los ")
        pdf.line(175, 200, 210, 200)

        pdf.drawString(210, 200, u"días del mes de")
        pdf.line(280, 200, 358, 200)

        pdf.drawString(360, 200, u"del año")
        pdf.line(400, 200, 430, 200)

        return queryset
 
    def get_context_data(self, **kwargs):
        context = super(generarF6, self).get_context_data(**kwargs)
        carnet_estudiante = self.kwargs.get('carnet_estudiante')
        context['carnet_estudiante'] = carnet_estudiante
        return context
         
    def get(self, request, *args, **kwargs):
        #Indicamos el tipo de contenido a devolver, en este caso un pdf
        response = HttpResponse(content_type='application/pdf')

        pdf_name = "Comprobante_F6_UPS.pdf"
        # Esta linea es por si deseas descargar el pdf a tu computadora
        response['Content-Disposition'] = 'inline; filename=%s' % pdf_name

        #La clase io.BytesIO permite tratar un array de bytes como un fichero binario, se utiliza como almacenamiento temporal
        buffer = BytesIO()

        #Canvas nos permite hacer el reporte con coordenadas X y Y
        pdf = canvas.Canvas(buffer)

        #Llamo al método cabecera donde están definidos los datos que aparecen en la cabecera del reporte.
        self.cabecera(pdf)
        self.get_queryset(pdf)

        #Con show page hacemos un corte de página para pasar a la siguiente
        pdf.showPage()
        pdf.save()
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response



# #-----------------------------------------------------------------------------------------------


class generarF7(ListView):
    model = Estudiante
    template_name = 'app1/Estudiante.html'
    context_object_name = 'estudiante'
    success_url = reverse_lazy('proyeccionsocial:generar_F7')  
     
    def cabecera(self,pdf):
         #Utilizamos el archivo logo_django.png que está guardado en la carpeta media/imagenes
        archivo_imagen1 = settings.BASE_DIR+'/static/img/logoUPSAgro.png'
        archivo_imagen2 = settings.BASE_DIR+'/static/img/logoUES.jpg'

        #Definimos el tamaño de la imagen a cargar y las coordenadas correspondientes
        pdf.drawImage(archivo_imagen1, 50, 730, 125, 90,preserveAspectRatio=True) 
        pdf.drawImage(archivo_imagen2, 430, 720, 125, 90,preserveAspectRatio=True) 

        # Establecemos el tamaño de letra en 8 y el tipo de letra Helvetica en negrita
        # Luego en drawString se colocan las coordenadas X Y de donde se quiere poner
        # el texto, el eje Y inicia en la parte inferior izquierda, ahi es el punto (0, 0)
        pdf.setFont("Helvetica-Bold", 8)
        pdf.drawString(248, 780, u"UNIVERSIDAD DE EL SALVADOR")

        pdf.setFont("Helvetica-Bold", 8)
        pdf.drawString(232, 770, u"FACULTAD DE CIENCIAS AGRONOMICAS")  

        pdf.setFont("Helvetica-Bold", 8)
        pdf.drawString(234, 760, u"UNIDAD DE DESARROLLO ACADEMICO") 

        pdf.setFont("Helvetica-Bold", 8)
        pdf.drawString(245, 750, u"UNIDAD DE PROYECCION SOCIAL")         

    def get_queryset(self, pdf, **kwargs):
        carnet_estudiante = self.kwargs.get('carnet_estudiante')
        queryset = Estudiante.objects.filter(carnet_estudiante = carnet_estudiante)
        #Declaracion y asignacion de variables que se recuperaran de la BD
        nomproy= "Manejo de Base de Datos"
        nombre = "Robeto Carlos, Paz Ramirez"
        numExpediente= "12"
        departamento= "Inteligencia Informatica"
        entidad = "Facultad de Ingeneria y Arquitectura, UES"
        lugarPrestServ= "San Salvador"
        numInforme= 32
        fecha_inicio = "12/10/20"
        fecha_fin="12/10/21"
        horasrepActual="450"
        horasTot="500"
        sexo = "M"
        telefono = "7452-2749"
        correo = "rm17039@ues.edu.sv"
        direccion = "8va. Calle Poniente Barrio San Sebastian Analco Casa No. 38 A, Zacatecoluca, La Paz."
        carrera = "Ingenieria de Sistemas Informaicos"
        carnet = "RM17039"
        porc_carrera = 60
        und_valor = 100
        ciclo_lect = "Impar"
        experiencia = "Desarrollo y conocimiento en html, java, javascript, python, php, css etc. "
        horas_sem = 24
        dias_sem = 6
        modalidad = "Presencial"

        aceptado = "SI"
        motivo = "Faltan Datos"
        observaciones = "Buscar otra institucion y presentarla lo mas antes posible a la secretaria de proyeccion social"

        pdf.setFont("Helvetica-Bold", 26)
        pdf.drawString(100, 720, u"F-7")

        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(200, 710, u"FORMATO DEL INFORME DE SERVIVIO SOCIAL")

        cx=55
        cy=685
        ancho=500
        alto=20
        pdf.rect(cx, cy, ancho, alto)

        texto = 'NOMBRE DEL PROYECTO: %s' % nomproy
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 690, texto)

        cx=55
        cy=570
        ancho=500
        alto=100
        pdf.rect(cx, cy, ancho, alto)            

        texto = 'NOMBRE DEL ALUMNO: %s' % nombre
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 655, texto)

        texto = 'NÚMERO DE CARNÉ: %s' % carnet
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 635, texto)

        texto = 'No. EXPEDIENTE: %s' % numExpediente
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 615, texto)

        texto = 'DEPARTAMENTO: %s' % departamento
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 595, texto)

        texto = 'CARRERA: %s' % carrera
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 575, texto)       

        cx=55
        cy=515
        ancho=500
        alto=40
        pdf.rect(cx, cy, ancho, alto)            

        texto = 'ENTIDAD DONDE REALIZA EL SERVICIO: %s' % entidad
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 540, texto)                  

        texto = 'LUGAR DE PRESTACIÓN DEL SERVICIO SOCIAL: %s' % lugarPrestServ 
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 520, texto)   
        

        texto = 'NUMERO DE INFORME: %s' % numInforme 
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 485, texto) 

        cx=55
        cy=440
        ancho=500
        alto=60
        pdf.rect(cx, cy, ancho, alto)                   

        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 465, u'PERIODO REPORTADO: ')  

        texto = 'Del día:   %s' % fecha_inicio
        pdf.setFont("Helvetica", 10)
        pdf.drawString(180, 465, texto)      

        texto = ';al día:   %s' % fecha_fin
        pdf.setFont("Helvetica", 10)
        pdf.drawString(280, 465, texto)           

        texto = 'Total de horas de este reporte: %s' % horasrepActual
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 445, texto)                           

        texto = 'Total de horas Acumuladas: %s' % horasTot
        pdf.setFont("Helvetica", 10)
        pdf.drawString(250, 445, texto)  

        cx=55
        cy=355
        ancho=500
        alto=70
        pdf.rect(cx, cy, ancho, alto)   

        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 410, u'DESCRIPCIÓN DE ACTIVIDADES: Máximo 2 páginas en tamaño carta ')  

        texto = 'Se describira tofo lo que se haya dearrollado en las 250 horas dentro del proyecto de servicio social y de '
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 390, texto)  

        texto = 'acuerdo con lo programado en el cronograma de actividades. A si mismo, se indicara el cumplimiento o '
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 380, texto)  

        texto = 'incumplimeinto de dichas actividades indicando las razones. Tambien podran ser añadidas observaciones '
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 370, texto)       

        #########FIRMAS############

        x1 = 80
        y1 = 300
        x2= 280
        y2= 300
        pdf.line(x1, y1, x2, y2)

        texto = 'NOMBRE Y FIRMA TUTOR INTERNO'
        pdf.setFont("Helvetica", 10)
        pdf.drawString(90, 290, texto)
        pdf.drawString(160, 270, u'SELLO') 

        x1 = 330
        y1 = 300
        x2 = 530
        y2= 300
        pdf.line(x1, y1, x2, y2)

        texto = 'NOMBRE Y FIRMA TUTOR EXTERNO'
        pdf.setFont("Helvetica", 10)
        pdf.drawString(340, 290, texto) 
        pdf.drawString(410, 270, u'SELLO') 

        x1 = 205
        y1 = 230
        x2 = 405
        y2= 230
        pdf.line(x1, y1, x2, y2)

        texto = 'FIRMA DEL ESTUDIANTE'
        pdf.setFont("Helvetica", 10)
        pdf.drawString(245, 220, texto) 

        x1 = 205
        y1 = 160
        x2 = 405
        y2= 160
        pdf.line(x1, y1, x2, y2)

        texto = 'Vo. Bo. COORDINADOR DE PROYECCIÓN SOCIAL DEL DEPARTAMENTO'
        pdf.setFont("Helvetica", 10)
        pdf.drawString(135, 150, texto) 
        ##############################

        texto = 'NOTA: ESTE INFORME DEBERÁ SER PRESENTADO EN DIGITAL Y EN FISICO, CADA 250 HORAS,'
        pdf.setFont("Helvetica", 10)
        pdf.drawString(80, 120, texto)  

        texto = 'DENTRO DE LOS PRIMEROS 5 DÍAS HÁBILES DE LA FECHA DE TÉRMINO DEL MISMO, DE LO '
        pdf.setFont("Helvetica", 10)
        pdf.drawString(80, 110, texto)  

        texto = 'CONTRARIO PROCEDERÁ SANCIÓN DE ACUERDO AL REGLAMENTO VIGENTE'
        pdf.setFont("Helvetica", 10)
        pdf.drawString(80, 100, texto) 

        return queryset

    def get_context_data(self, **kwargs):
        context = super(generarF7, self).get_context_data(**kwargs)
        carnet_estudiante = self.kwargs.get('carnet_estudiante')
        context['carnet_estudiante'] = carnet_estudiante
        return context
         
    def get(self, request, *args, **kwargs):
        #Indicamos el tipo de contenido a devolver, en este caso un pdf
        response = HttpResponse(content_type='application/pdf')

        pdf_name = "Comprobante_F7_UPS.pdf"
        # Esta linea es por si deseas descargar el pdf a tu computadora
        response['Content-Disposition'] = 'inline; filename=%s' % pdf_name

        #La clase io.BytesIO permite tratar un array de bytes como un fichero binario, se utiliza como almacenamiento temporal
        buffer = BytesIO()

        #Canvas nos permite hacer el reporte con coordenadas X y Y
        pdf = canvas.Canvas(buffer)

        #Llamo al método cabecera donde están definidos los datos que aparecen en la cabecera del reporte.
        self.cabecera(pdf)
        self.get_queryset(pdf)

        #Con show page hacemos un corte de página para pasar a la siguiente
        pdf.showPage()
        pdf.save()
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response


# #------------------------------------------------------------------------------------------------------------------


class generarF8(ListView):
    model = Estudiante
    template_name = 'app1/Estudiante.html'
    context_object_name = 'estudiante'
    success_url = reverse_lazy('proyeccionsocial:generar_F1')  
     
    def cabecera(self,pdf):
         #Utilizamos el archivo logo_django.png que está guardado en la carpeta media/imagenes
        archivo_imagen1 = settings.BASE_DIR+'/static/img/logoUPSAgro.png'
        archivo_imagen2 = settings.BASE_DIR+'/static/img/logoUES.jpg'

        #Definimos el tamaño de la imagen a cargar y las coordenadas correspondientes
        pdf.drawImage(archivo_imagen1, 50, 730, 125, 90,preserveAspectRatio=True) 
        pdf.drawImage(archivo_imagen2, 430, 720, 125, 90,preserveAspectRatio=True) 

        #Establecemos el tamaño de letra en 8 y el tipo de letra Helvetica en negrita
        #Luego en drawString se colocan las coordenadas X Y de donde se quiere poner
        #el texto, el eje Y inicia en la parte inferior izquierda, ahi es el punto (0, 0)
        pdf.setFont("Helvetica-Bold", 8)
        pdf.drawString(248, 780, u"UNIVERSIDAD DE EL SALVADOR")

        pdf.setFont("Helvetica-Bold", 8)
        pdf.drawString(232, 770, u"FACULTAD DE CIENCIAS AGRONOMICAS")  

        pdf.setFont("Helvetica-Bold", 8)
        pdf.drawString(234, 760, u"UNIDAD DE DESARROLLO ACADEMICO") 

        pdf.setFont("Helvetica-Bold", 8)
        pdf.drawString(245, 750, u"UNIDAD DE PROYECCION SOCIAL")        

    def get_queryset(self, pdf, **kwargs):
        carnet_estudiante = self.kwargs.get('carnet_estudiante')
        queryset = Estudiante.objects.filter(carnet_estudiante = carnet_estudiante)

        for i in Estudiante.objects.filter(carnet_estudiante = carnet_estudiante):
            carnet = i.carnet_estudiante
            nombre = i.nombre_estudiante
            apellido = i.apellido_estudiante

        for i in EstudioUniversitario.objects.filter(carnet_estudiante = carnet_estudiante):
            carrera = i.codigo_carrera.nombre_carrera

        for i in Solicitud.objects.filter(carnet_estudiante = carnet_estudiante):
            fecha_fin = i.fecha_fin
            fecha_inicio = i.fecha_inicio
        
        docenteTutor = "Marcia Lizeth Rivera García"

        pdf.setFont("Helvetica-Bold", 26)
        pdf.drawString(100, 720, u"F-8")

        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(60, 690, u"HOJA DE REGISTRO DE LAS HORAS SOCIALES REALIZADAS EN LA ESTACIÓN EXPERIMENTAL Y DE")
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(180, 675, u"PRÁCTICAS POR ESTUDIANTES DE LA UNIVERSIDAD")

        texto = 'Nombre Completo:   %s' % nombre +' '+ apellido
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 630, texto)

        texto = 'Carnet No.:    %s' % carnet
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 610, texto)

        texto = 'Carrera:   %s' % carrera
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 590, texto)

        texto = 'Docente Tutor:   %s' % docenteTutor
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 570, texto)

        cx=60
        cy=515
        ancho=55
        alto=40
        pdf.rect(cx, cy, ancho, alto)

        texto = 'FECHA'
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(70, 530, texto)

        cx=115
        cy=515
        ancho=57
        alto=40
        pdf.rect(cx, cy, ancho, alto)

        texto = 'HORA DE'
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(121, 535, texto)

        texto = 'ENTRADA'
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(120, 525, texto)

        cx=172
        cy=515
        ancho=250
        alto=40
        pdf.rect(cx, cy, ancho, alto)

        texto = 'ACTIVIDAD REALIZADA'
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(235, 530, texto)

        cx=422
        cy=515
        ancho=57
        alto=40
        pdf.rect(cx, cy, ancho, alto)

        texto = 'HORA DE'
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(428, 535, texto)

        texto = 'SALIDA'
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(432, 525, texto)

        cx=479
        cy=515
        ancho=70
        alto=40
        pdf.rect(cx, cy, ancho, alto)

        texto = 'HORAS'
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(495, 535, texto)

        texto = 'REALIZADAS'
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(483, 525, texto)

    #-------------- FILA 1 ------------------------------        

        cx=60
        cy=490
        ancho=55
        alto=25
        pdf.rect(cx, cy, ancho, alto)

        cx=115
        cy=490
        ancho=57
        alto=25
        pdf.rect(cx, cy, ancho, alto)

        cx=172
        cy=490
        ancho=250
        alto=25
        pdf.rect(cx, cy, ancho, alto)

        cx=422
        cy=490
        ancho=57
        alto=25
        pdf.rect(cx, cy, ancho, alto)

        cx=479
        cy=490
        ancho=70
        alto=25
        pdf.rect(cx, cy, ancho, alto)

    #-------------- FILA 2 ------------------------------   

        cx=60
        cy=465
        ancho=55
        alto=25
        pdf.rect(cx, cy, ancho, alto)

        cx=115
        cy=465
        ancho=57
        alto=25
        pdf.rect(cx, cy, ancho, alto)

        cx=172
        cy=465
        ancho=250
        alto=25
        pdf.rect(cx, cy, ancho, alto)

        cx=422
        cy=465
        ancho=57
        alto=25
        pdf.rect(cx, cy, ancho, alto)

        cx=479
        cy=465
        ancho=70
        alto=25
        pdf.rect(cx, cy, ancho, alto)

    #-------------- FILA 3 ------------------------------   

        cx=60
        cy=440
        ancho=55
        alto=25
        pdf.rect(cx, cy, ancho, alto)

        cx=115
        cy=440
        ancho=57
        alto=25
        pdf.rect(cx, cy, ancho, alto)

        cx=172
        cy=440
        ancho=250
        alto=25
        pdf.rect(cx, cy, ancho, alto)

        cx=422
        cy=440
        ancho=57
        alto=25
        pdf.rect(cx, cy, ancho, alto)

        cx=479
        cy=440
        ancho=70
        alto=25
        pdf.rect(cx, cy, ancho, alto)

    #-------------- FILA 4 ------------------------------   

        cx=60
        cy=415
        ancho=55
        alto=25
        pdf.rect(cx, cy, ancho, alto)

        cx=115
        cy=415
        ancho=57
        alto=25
        pdf.rect(cx, cy, ancho, alto)

        cx=172
        cy=415
        ancho=250
        alto=25
        pdf.rect(cx, cy, ancho, alto)

        cx=422
        cy=415
        ancho=57
        alto=25
        pdf.rect(cx, cy, ancho, alto)

        cx=479
        cy=415
        ancho=70
        alto=25
        pdf.rect(cx, cy, ancho, alto)

    #-------------- FILA 5 ------------------------------   

        cx=60
        cy=390
        ancho=55
        alto=25
        pdf.rect(cx, cy, ancho, alto)

        cx=115
        cy=390
        ancho=57
        alto=25
        pdf.rect(cx, cy, ancho, alto)

        cx=172
        cy=390
        ancho=250
        alto=25
        pdf.rect(cx, cy, ancho, alto)

        cx=422
        cy=390
        ancho=57
        alto=25
        pdf.rect(cx, cy, ancho, alto)

        cx=479
        cy=390
        ancho=70
        alto=25
        pdf.rect(cx, cy, ancho, alto)

    #-------------- FILA 6 ------------------------------   

        cx=60
        cy=365
        ancho=55
        alto=25
        pdf.rect(cx, cy, ancho, alto)

        cx=115
        cy=365
        ancho=57
        alto=25
        pdf.rect(cx, cy, ancho, alto)

        cx=172
        cy=365
        ancho=250
        alto=25
        pdf.rect(cx, cy, ancho, alto)

        cx=422
        cy=365
        ancho=57
        alto=25
        pdf.rect(cx, cy, ancho, alto)

        cx=479
        cy=365
        ancho=70
        alto=25
        pdf.rect(cx, cy, ancho, alto)

    #---------------------------------------------------------------- 

        texto = 'Este registro de actividades comprende del día:    %s' %fecha_inicio
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 330, texto)

        texto = ';Al día:   %s' %fecha_fin
        pdf.setFont("Helvetica", 10)
        pdf.drawString(340, 330, texto)

    # ----------- FIRMAS ----------------#

        x1 = 100
        y1 = 280
        x2 = 500
        y2 = 280
        pdf.line(x1, y1, x2, y2)

        texto = 'NOMBRE Y FIRMA DEL COORDINADOR DE LA EXTENSION AGROPECUARIA DE LA EEP'
        pdf.setFont("Helvetica", 10)
        pdf.drawString(90, 260, texto)

        x1 = 100
        y1 = 200
        x2 = 500
        y2 = 200
        pdf.line(x1, y1, x2, y2)

        texto = 'Vo. Bo. DIRECTOR DE LA ESTACIÓN EXPERIMENTAL Y DE PRÁCTICAS'
        pdf.setFont("Helvetica", 10)
        pdf.drawString(130, 180, texto) 

        texto = 'SELLO'
        pdf.setFont("Helvetica", 10)
        pdf.drawString(285, 130, texto) 

        x1 = 180
        y1 = 90
        x2 = 430
        y2 = 90
        pdf.line(x1, y1, x2, y2)

        texto = 'NOMBRE Y FIRMA DEL DOCENTE TUTOR'
        pdf.setFont("Helvetica", 10)
        pdf.drawString(200, 70, texto)

    # ----------------------------------------- #

        return queryset

    def get_context_data(self, **kwargs):
        context = super(generarF1, self).get_context_data(**kwargs)
        carnet_estudiante = self.kwargs.get('carnet_estudiante')
        context['carnet_estudiante'] = carnet_estudiante
        return context
         
    def get(self, request, *args, **kwargs):
        #Indicamos el tipo de contenido a devolver, en este caso un pdf
        response = HttpResponse(content_type='application/pdf')

        pdf_name = "Comprobante_F8_UPS.pdf"
        # Esta linea es por si deseas descargar el pdf a tu computadora
        response['Content-Disposition'] = 'inline; filename=%s' % pdf_name

        #La clase io.BytesIO permite tratar un array de bytes como un fichero binario, se utiliza como almacenamiento temporal
        buffer = BytesIO()

        #Canvas nos permite hacer el reporte con coordenadas X y Y
        pdf = canvas.Canvas(buffer)

        #Llamo al método cabecera donde están definidos los datos que aparecen en la cabecera del reporte.
        self.cabecera(pdf)
        self.get_queryset(pdf)

        #Con show page hacemos un corte de página para pasar a la siguiente
        pdf.showPage()
        pdf.save()
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response


# #-----------------------------------------------------------------------------------------------


class generarF9(ListView):
    model = Estudiante
    template_name = 'app1/Estudiante.html'
    context_object_name = 'estudiante'
    success_url = reverse_lazy('proyeccionsocial:generar_F9')  
     
    def cabecera(self,pdf):
         #Utilizamos el archivo logo_django.png que está guardado en la carpeta media/imagenes
        archivo_imagen1 = settings.BASE_DIR+'/static/img/logoUPSAgro.png'
        archivo_imagen2 = settings.BASE_DIR+'/static/img/logoUES.jpg'

        #Definimos el tamaño de la imagen a cargar y las coordenadas correspondientes
        pdf.drawImage(archivo_imagen1, 50, 730, 125, 90,preserveAspectRatio=True) 
        pdf.drawImage(archivo_imagen2, 430, 720, 125, 90,preserveAspectRatio=True) 

        # Establecemos el tamaño de letra en 8 y el tipo de letra Helvetica en negrita
        # Luego en drawString se colocan las coordenadas X Y de donde se quiere poner
        # el texto, el eje Y inicia en la parte inferior izquierda, ahi es el punto (0, 0)
        pdf.setFont("Helvetica-Bold", 8)
        pdf.drawString(248, 780, u"UNIVERSIDAD DE EL SALVADOR")

        pdf.setFont("Helvetica-Bold", 8)
        pdf.drawString(232, 770, u"FACULTAD DE CIENCIAS AGRONOMICAS")  

        pdf.setFont("Helvetica-Bold", 8)
        pdf.drawString(234, 760, u"UNIDAD DE DESARROLLO ACADEMICO") 

        pdf.setFont("Helvetica-Bold", 8)
        pdf.drawString(245, 750, u"UNIDAD DE PROYECCION SOCIAL")     

    def get_queryset(self, pdf, **kwargs):
        carnet_estudiante = self.kwargs.get('carnet_estudiante')
        queryset = Estudiante.objects.filter(carnet_estudiante = carnet_estudiante)
        #Declaracion y asignacion de variables que se recuperaran de la BD
        numero = 1
        nombre = "Noel Alexander Renderos Martinez"
        sexo = "M"
        telefono = "7452-2749"
        correo = "rm17039@ues.edu.sv"
        direccion = "8va. Calle Poniente Barrio San Sebastian Analco Casa No. 38 A, Zacatecoluca, La Paz."
        carrera = "Ingenieria de Sistemas Informaicos"
        carnet = "RM17039"
        porc_carrera = 60
        und_valor = 100
        ciclo_lect = "Impar"
        experiencia = "Desarrollo y conocimiento en html, java, javascript, python, php, css etc. "
        horas_sem = 24
        dias_sem = 6
        entidad = "Facultad de Ingeneria y Arquitectura, UES"
        modalidad = "Presencial"
        fecha_inicio = "12/10/20"
        fecha_fin= "12/10/21"
        aceptado = "SI"
        motivo = "Faltan Datos"
        observaciones = "Buscar otra institucion y presentarla lo mas antes posible a la secretaria de proyeccion social"

        pdf.setFont("Helvetica-Bold", 26)
        pdf.drawString(100, 715, u"F-9")

        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(90, 660, u"CONSTANCIA HORAS SOCIALES EN LA ESTACIÓN EXPERIMENTAL Y DE PRÁCTICAS")

        texto = 'El suscrito, coordinador de Extensión Agropecuaria de la Estación Experimental y de Prácticas, ' 
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 620, texto)

        texto = 'hace constar que el(la)' 
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 600, texto)

        texto = 'Bachiller:   %s' % nombre
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 580, texto)   

        texto = 'Carné No.: %s' % carnet
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 560, texto)    

        texto = 'matriculado(a) en la carrera:'
        pdf.setFont("Helvetica", 10)
        pdf.drawString(200, 560, texto)        

        texto = '%s' % carrera
        pdf.setFont("Helvetica", 10)
        pdf.drawString(180, 540, texto)  

        x1 = 60
        y1 = 525
        x2 = 530
        y2 = 525
        pdf.line(x1, y1, x2, y2)    

        texto = 'ha cumplido satisfactoriamnet las horas sociales correspondientes al 25% de su servicio social en'
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 500, texto)   

        texto = 'esta unidad, conforme al plan de trabajo diseñado para el perido:'
        pdf.drawString(60, 480, texto)   

        texto = 'Del día:  %s' % fecha_inicio
        pdf.setFont("Helvetica", 10)
        pdf.drawString(180, 460, texto)      

        texto = ';al día:  %s' % fecha_fin
        pdf.setFont("Helvetica", 10)
        pdf.drawString(265, 460, texto) 

        x1 = 60
        y1 = 150
        x2 = 520
        y2 = y1
        pdf.line(x1, y1, x2, y2)

        texto = 'NOMBRE Y FIRMA DEL DOCENTE TUTOR'
        pdf.setFont("Helvetica", 10)
        pdf.drawString(200, 140, texto) 

        x1 = 60
        y1 = 250
        x2 = 520
        y2 = y1
        pdf.line(x1, y1, x2, y2)

        texto = 'Vo. Bo. DIRECTOR DE LA ESTACIÓN EXPERIMENTAL Y DE PRÁCTICAS'
        pdf.setFont("Helvetica", 10)
        pdf.drawString(130, 240, texto)
        pdf.drawString(270, 220, u'SELLO')         

        x1 = 60
        y1 = 350
        x2 = 520
        y2 = y1
        pdf.line(x1, y1, x2, y2)

        texto = 'NOMBRE Y FIRMA DEL COORDINADOR DE EXTENSION AGROPECUARIA'
        pdf.setFont("Helvetica", 10)
        pdf.drawString(130, 330, texto)

        return queryset
 
    def get_context_data(self, **kwargs):
        context = super(generarF9, self).get_context_data(**kwargs)
        carnet_estudiante = self.kwargs.get('carnet_estudiante')
        context['carnet_estudiante'] = carnet_estudiante
        return context
         
    def get(self, request, *args, **kwargs):
        #Indicamos el tipo de contenido a devolver, en este caso un pdf
        response = HttpResponse(content_type='application/pdf')

        pdf_name = "Comprobante_F9_UPS.pdf"
        # Esta linea es por si deseas descargar el pdf a tu computadora
        response['Content-Disposition'] = 'inline; filename=%s' % pdf_name

        #La clase io.BytesIO permite tratar un array de bytes como un fichero binario, se utiliza como almacenamiento temporal
        buffer = BytesIO()

        #Canvas nos permite hacer el reporte con coordenadas X y Y
        pdf = canvas.Canvas(buffer)

        #Llamo al método cabecera donde están definidos los datos que aparecen en la cabecera del reporte.
        self.cabecera(pdf)
        self.get_queryset(pdf)

        #Con show page hacemos un corte de página para pasar a la siguiente
        pdf.showPage()
        pdf.save()
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response


# #------------------------------------------------------------------------------------------------------------------


class generarF11(ListView):
    model = Estudiante
    template_name = 'app1/Estudiante.html'
    context_object_name = 'Estudiante'
    success_url = reverse_lazy('proyeccionsocial:generar_F11')  

    def cabecera(self,pdf):
         #Utilizamos el archivo logo_django.png que está guardado en la carpeta media/imagenes
        archivo_imagen1 = settings.BASE_DIR+'/static/img/logoUPSAgro.png'
        archivo_imagen2 = settings.BASE_DIR+'/static/img/logoUES.jpg'

        #Definimos el tamaño de la imagen a cargar y las coordenadas correspondientes
        pdf.drawImage(archivo_imagen1, 50, 730, 125, 90,preserveAspectRatio=True) 
        pdf.drawImage(archivo_imagen2, 430, 720, 125, 90,preserveAspectRatio=True) 

        # Establecemos el tamaño de letra en 8 y el tipo de letra Helvetica en negrita
        # Luego en drawString se colocan las coordenadas X Y de donde se quiere poner
        # el texto, el eje Y inicia en la parte inferior izquierda, ahi es el punto (0, 0)
        pdf.setFont("Helvetica-Bold", 8)
        pdf.drawString(248, 780, u"UNIVERSIDAD DE EL SALVADOR")

        pdf.setFont("Helvetica-Bold", 8)
        pdf.drawString(232, 770, u"FACULTAD DE CIENCIAS AGRONOMICAS")  

        pdf.setFont("Helvetica-Bold", 8)
        pdf.drawString(234, 760, u"UNIDAD DE DESARROLLO ACADEMICO") 

        pdf.setFont("Helvetica-Bold", 8)
        pdf.drawString(245, 750, u"UNIDAD DE PROYECCION SOCIAL")     

    def get_queryset(self, pdf, **kwargs):
        carnet_estudiante = self.kwargs.get('carnet_estudiante')
        queryset = Estudiante.objects.filter(carnet_estudiante = carnet_estudiante)
        #Declaracion y asignacion de variables que se recuperaran de la BD

        nombre = "Karla María Abrego Reyes"
        nombre_proyecto = "NOSE"
        
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(90, 700, u"FICHA DE EVALUACIÓN DE DESEMPEÑO DEL ESTUDIANTE POR EL TUTOR EXTERNO")

        pdf.setFont("Helvetica-Bold", 26)
        pdf.drawString(100, 723, u"F11")

        texto = 'Nombre del alumno:   %s' % nombre
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 675, texto)

        texto = 'Nombre del proyecto:   %s' % nombre_proyecto
        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 650, texto)

        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, 620, u"Señala con un X en el cuadro correspondiente,la calificación a la que el estudiante se hizo acreedor durante")
        pdf.drawString(60, 605, u"la realización del Servicio Social; su dictamen será tomado en cuenta para la evolucion del estudiante.Le")
        pdf.drawString(60, 590,u"solicitamos nos haga llegar este documento en forma confidencial cuando el alumno haya terminado el período")
        pdf.drawString(60, 575, u"de actividades a las que se compremetió con su entidad.")

        pdf.drawString(60, 545, u"Categorías de evaluación: Deficiente: D, Regular: R, Bueno: B, Excelente: E")

        #Generando tabla!

        pdf.line(90, 530, 540, 530) #linea horizontal 
        pdf.line(290, 505, 540,505) #linea horizontal 
        pdf.line(90, 490, 540, 490) #linea horizontal
        pdf.line(90, 462, 540, 462) #linea horizontal
        pdf.line(90, 447, 540, 447) #linea horizontal
        pdf.line(90, 432, 540, 432) #linea horizontal
        pdf.line(90, 417, 540, 417) #linea horizontal
        pdf.line(90, 402, 540, 402) #linea horizontal
        pdf.line(90, 387, 540, 387) #linea horizontal
        pdf.line(90, 372, 540, 372) #linea horizontal
        pdf.line(90, 357, 540, 357) #linea hotizontal
        pdf.line(90, 342, 540, 342) #linea horizontal
        pdf.line(90, 327, 540, 327) #linea horizontal
        pdf.line(90, 312, 540, 312) #linea horizontal
        pdf.line(90, 297, 540, 297) #linea horizontal
        pdf.line(90, 282, 540, 282) #linea horizontal
        pdf.line(90, 267, 540, 267) #linea horizontal
        pdf.line(90, 252, 540, 252) #linea horizontal
        pdf.line(90, 237, 540, 237) #linea horizontal

        pdf.line(90, 530, 90, 237) #linea vertical
        pdf.line(290,530, 290, 237)

        pdf.line(353,505, 353, 237)
        pdf.line(415,505, 415, 237)
        pdf.line(478,505, 478, 237)

        pdf.line(540, 530, 540, 237) #linea vertical

        pdf.setFont("Helvetica", 10)
        pdf.drawString(120, 508, u"FACTORES DE EVALUACIÓN")
        pdf.drawString(380, 512, u"CATEGORÍAS")

        pdf.drawString(95,480, u"1. Responsabilidad en el cumplimiento de")
        pdf.drawString(95,467, u"   las actividades encomendadas")
        pdf.drawString(95,452, u"2. Evolución en el aprendizaje")
        pdf.drawString(95,437, u"3. Capacidad técnica")
        pdf.drawString(95,422, u"4. Receptividad a las indicaciones dadas")
        pdf.drawString(95,407, u"5. Iniciativa")
        pdf.drawString(95,392, u"6. Capacidad para transmitir ideas")
        pdf.drawString(95,377, u"7. Capacidad analítica")
        pdf.drawString(95,362, u"8. Creatividad")
        pdf.drawString(95,347, u"9. Integridad moral y ética")
        pdf.drawString(95,332, u"10.Puntulidad")
        pdf.drawString(95,317, u"11.Disciplina")
        pdf.drawString(95,302, u"12.Integración social ")
        pdf.drawString(95,287, u"13.Integración en equipo")
        pdf.drawString(95,272, u"14.Represntación personal")
        pdf.drawString(95,257, u"15.Respeto")
        pdf.drawString(95,242, u"16.Cooperación")
        pdf.drawString(298,493, u"Excelente")
        pdf.drawString(370,493, u"Bueno")
        pdf.drawString(430,493, u"Regular")
        pdf.drawString(487,493, u"Deficiente")

        pdf.drawString(60,205, u"Nombre y firma del tutor externo:")
        pdf.line(212, 205, 500, 205) #linea horizontal

        pdf.drawString(60,180, u"Nombre y firma del presentante de la entidad:")
        pdf.line(265, 180, 500, 180) #linea horizontal

        pdf.drawString(60,155, u"Lugar y fecha:")
        pdf.line(125, 155, 500, 155) #linea horizontal

        return queryset
 
    def get_context_data(self, **kwargs):
        context = super(generarF11, self).get_context_data(**kwargs)
        carnet_estudiante = self.kwargs.get('carnet_estudiante')
        context['carnet_estudiante'] = carnet_estudiante
        return context
         
    def get(self, request, *args, **kwargs):
        #Indicamos el tipo de contenido a devolver, en este caso un pdf
        response = HttpResponse(content_type='application/pdf')

        pdf_name = "Comprobante_F11_UPS.pdf"
        # Esta linea es por si deseas descargar el pdf a tu computadora
        response['Content-Disposition'] = 'inline; filename=%s' % pdf_name

        #La clase io.BytesIO permite tratar un array de bytes como un fichero binario, se utiliza como almacenamiento temporal
        buffer = BytesIO()

        #Canvas nos permite hacer el reporte con coordenadas X y Y
        pdf = canvas.Canvas(buffer)

        #Llamo al método cabecera donde están definidos los datos que aparecen en la cabecera del reporte.
        self.cabecera(pdf)
        self.get_queryset(pdf)

        #Con show page hacemos un corte de página para pasar a la siguiente
        pdf.showPage()
        pdf.save()
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response