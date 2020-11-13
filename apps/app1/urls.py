from django.urls import path, include
from .views import *
from django.contrib.auth.decorators import login_required


app_name='proyeccionsocial'

urlpatterns=[
	#URL para el menu de inicio
	#path('', index),
	path('proyeccionsocial/index/<username>',login_required(index), name='index'),


	#URL para Ciclo
	path('proyeccionsocial/consultaCiclo/',login_required(consultaCiclo), name="consulta_ciclo"),
	path('proyeccionsocial/crearCiclo/',login_required(crearCiclo.as_view()), name="crear_ciclo"),
	path('proyeccionsocial/editarCiclo/<pk>/',login_required(editarCiclo.as_view()), name="editar_ciclo"),
	path('proyeccionsocial/eliminarCiclo/<pk>/',login_required(eliminarCiclo.as_view()), name="eliminar_ciclo"),


	#URL para Estudiante
	path('proyeccionsocial/consultaEstudiante/<username>/',login_required(consultaEstudiante), name="consulta_estudiante"),
	path('proyeccionsocial/crearEstudiante/<username>/',login_required(crearEstudiante.as_view()), name="crear_estudiante"),
	path('proyeccionsocial/editarEstudiante/<pk>/',login_required(editarEstudiante.as_view()), name="editar_estudiante"),
	path('proyeccionsocial/eliminarEstudiante/<pk>/',login_required(eliminarEstudiante.as_view()), name="eliminar_estudiante"),
	#Buscar Estudiante
	path('proyeccionsocial/consultaEstudianteBuscar/',login_required(consultaEstudianteBuscar), name="consulta_estudiante_buscar"),


	#URL para Estudio Universitario
	path('proyeccionsocial/consultaEstudioUniversitario/<username>/',login_required(consultaEstudioUniversitario), name="consulta_estudio_universitario"),
	path('proyeccionsocial/crearEstudioUniversitario/<username>/',login_required(crearEstudioUniversitario.as_view()), name="crear_estudio_universitario"),
	path('proyeccionsocial/editarEstudioUniversitario/<pk>/',login_required(editarEstudioUniversitario.as_view()), name="editar_estudio_universitario"),
	path('proyeccionsocial/eliminarEstudioUniversitario/<pk>/',login_required(eliminarEstudioUniversitario.as_view()), name="eliminar_estudio_universitario"),
	#Buscar Estudio Universitario
	path('proyeccionsocial/consultaEstudioUniversitarioBuscar/',login_required(consultaEstudioUniversitarioBuscar), name="consulta_estudio_universitario_buscar"),


	#URL para la Solicitud de Servicio Social
	path('proyeccionsocial/consultaSolicitudServicioSocial/<username>/',login_required(consultaSolicitudServicioSocial), name="consulta_solicitud_servicio_social"),
	path('proyeccionsocial/crearSolicitudServicioSocial/<username>/',login_required(crearSolicitudServicioSocial.as_view()), name="crear_solicitud_servicio_social"),
	path('proyeccionsocial/editarSolicitudServicioSocial/<pk>/',login_required(editarSolicitudServicioSocial.as_view()), name="editar_solicitud_servicio_social"),
	path('proyeccionsocial/eliminarSolicitudServicioSocial/<pk>/',login_required(eliminarSolicitudServicioSocial.as_view()), name="eliminar_solicitud_servicio_social"),
	#Buscar Solicitud Servicio Social
	path('proyeccionsocial/consultaSolicitudServicioSocialBuscar/',login_required(consultaSolicitudServicioSocialBuscar), name="consulta_solicitud_servicio_social_buscar"),
	# Para el boton Solicitudes del Base para Administrador
	path('proyeccionsocial/editarSolicitudServicioSocial2/<pk>/',login_required(editarSolicitudServicioSocial2.as_view()), name="editar_solicitud_servicio_social2"),
	path('proyeccionsocial/eliminarSolicitudServicioSocial2/<pk>/',login_required(eliminarSolicitudServicioSocial2.as_view()), name="eliminar_solicitud_servicio_social2"),


	#URL para el Estado de la Solicitud de Servicio Social
	path('proyeccionsocial/consultaEstadoSolicitudServicioSocial/<username>/',login_required(consultaEstadoSolicitudServicioSocial), name="consulta_estado_solicitud_servicio_social"),
	path('proyeccionsocial/crearEstadoSolicitudServicioSocial/<username>/',login_required(crearEstadoSolicitudServicioSocial.as_view()), name="crear_estado_solicitud_servicio_social"),
	path('proyeccionsocial/editarEstadoSolicitudServicioSocial/<pk>/',login_required(editarEstadoSolicitudServicioSocial.as_view()), name="editar_estado_solicitud_servicio_social_consulta"),
	path('proyeccionsocial/eliminarEstadoSolicitudServicioSocial/<pk>/',login_required(eliminarEstadoSolicitudServicioSocial.as_view()), name="eliminar_estado_solicitud_servicio_social"),
	# Para el boton Solicitudes del Base para Administrador
	path('proyeccionsocial/consultaEstadoSolicitudServicioSocialConsulta/<username>/',login_required(consultaEstadoSolicitudServicioSocialConsulta), name="consulta_estado_solicitud_servicio_social_consulta"),
	path('proyeccionsocial/crearEstadoSolicitudServicioSocial2/<username>/',login_required(crearEstadoSolicitudServicioSocial2.as_view()), name="crear_estado_solicitud_servicio_social2"),
	path('proyeccionsocial/consultaEstadoSolicitudServicioSocialBuscar/',login_required(consultaEstadoSolicitudServicioSocialBuscar), name="consulta_estado_solicitud_servicio_social_buscar"),
	path('proyeccionsocial/consultaEstadoSolicitudServicioSocialBuscar2/',login_required(consultaEstadoSolicitudServicioSocialBuscar2), name="consulta_estado_solicitud_servicio_social_buscar2"),
	


	#URL para los Formularios
	path('proyeccionsocial/generarF1/<str:carnet_estudiante>/',login_required(generarF1.as_view()), name= "generar_F1"),
	path('proyeccionsocial/generarF2/<str:carnet_estudiante>/',login_required(generarF2.as_view()), name= "generar_F2"),
	path('proyeccionsocial/generarF3/<str:carnet_estudiante>/',login_required(generarF3.as_view()), name= "generar_F3"),
	path('proyeccionsocial/generarF4TI/<str:carnet_estudiante>/',login_required(generarF4TI.as_view()), name= "generar_F4TI"),
	path('proyeccionsocial/generarF4TE/<str:carnet_estudiante>/',login_required(generarF4TE.as_view()), name= "generar_F4TE"),
	path('proyeccionsocial/generarF6/<str:carnet_estudiante>/',login_required(generarF6.as_view()), name= "generar_F6"),
	path('proyeccionsocial/generarF7/<str:carnet_estudiante>/',login_required(generarF7.as_view()), name= "generar_F7"),
	path('proyeccionsocial/generarF8/<str:carnet_estudiante>/',login_required(generarF8.as_view()), name= "generar_F8"),
	path('proyeccionsocial/generarF9/<str:carnet_estudiante>/',login_required(generarF9.as_view()), name= "generar_F9"),
	path('proyeccionsocial/generarF11/<str:carnet_estudiante>/',login_required(generarF11.as_view()), name= "generar_F11"),
]