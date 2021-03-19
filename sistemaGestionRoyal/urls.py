"""sistemaGestionRoyal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include 
from rest_framework import routers                      # add this
from sistema import views
from django.conf import settings
from django.conf.urls.static import static

#router = routers.DefaultRouter()                        # add this
#router.register(r'Alumnos', views.AlumnoSerializer, 'Alumnos')   

urlpatterns = [
    url(r'^', include('sistema.urls')),#las apis
    path('admin/', admin.site.urls),
    path('', views.inicio, name='inicio'),
    path('logout', views.logoutUser, name='logout'),
    path('home/', views.base, name='home'),
    path('consulta_a/', views.consultar_a, name='consultar_a'),
    path('royalApp/', views.royalAppPassword, name='royalApp'),
    path('royalApp/<int:alumno>', views.modalAlumnos, name='royalApp'),
    path('consulta_a/<int:alumno>', views.modalAlumnos),
    path('consulta_d/', views.consultar_d, name='consultar_d'),
    path('consulta_d/<int:id>', views.modalDocentes),
    path('certificados/', views.certificados, name='certificados'),
    path('certificados/<int:id_alumno>/', views.modalcertificadoscombos),
    path('certificados/eliminar/<int:id>', views.modalcertificados),
    path('curso/', views.curso, name='cursos'),
    path('curso/<int:id>/', views.modalCursos),
    path('aula/', views.aula, name='aula'),
    path('aula/<int:id>/', views.modalAulas),
    path('grupos/', views.grupos, name='grupos'),
    path('grupos/<int:id>/', views.modalgrupos),
    path('grupos/<int:id_alumno>/<int:id_grupo>/<int:movimiento>/', views.moverAlumnos),
    path('gruposAulas/<int:id_aula>/<int:id_grupo>/<int:movimiento>/', views.moverAulas),
    path('pagos/', views.pagos, name='pagos'),
    path('pagos/<int:id_pago>/', views.modalPagos),
    path('registro/', views.modalPagos),
    path('registro/<int:id_alumno>/', views.modalPagos),
    path('promociones/', views.promociones, name='promociones'),
    path('promociones/<int:id>/', views.modalpromociones),
    path('pagos_d/', views.pagos_d, name='pagos_d'),
    path('pagos_d/<int:id_pago>/', views.modalPagosD),
    path('ventas/', views.ventas, name='ventas'),
    path('libros/', views.libros, name='libros'),
    path('libros/<int:id>/', views.modalLibros),
    path('inventario/', views.inventario, name='inventario'),
    path('inventario/<int:id>/', views.modalProducto),
    path('caja/', views.caja, name='caja'),
    path('cajacierre/', views.cajacierre, name='cajacierre'),
    path('historialVentas/', views.historialVentas, name='historialVentas'),
    path('caja/<int:id>/', views.modalDetalleVenta)
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)