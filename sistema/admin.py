from django.contrib import admin
from .models import Alumno,Docente,Producto,Certificado,Curso,Grupo,Aula,Pago,rel_alu_doc_grupo,rel_aula_grupo,Venta,Detalle_venta
# Register your models here.

class AlumnoRegistrado(admin.ModelAdmin):
    list_display = ["apellido","nombre","fechareg","fechaultmod"]
    list_filter = ["apellido","fecha_nacimiento"]
    search_fields = ["apellido","nombre"]
    class Meta:
        Model = Alumno
admin.site.register(Alumno,AlumnoRegistrado)
class DocenteRegistrado(admin.ModelAdmin):
    list_display = ["apellido","nombre","fechareg","fechaultmod"]
    list_filter = ["apellido","rfc"]
    search_fields = ["apellido","nombre"]
    class Meta:
        Model = Docente
admin.site.register(Docente,DocenteRegistrado)
admin.site.register(Producto)
admin.site.register(Certificado)
admin.site.register(Aula)
admin.site.register(Grupo)
admin.site.register(Curso)
admin.site.register(Pago)
admin.site.register(rel_alu_doc_grupo)
admin.site.register(rel_aula_grupo)
admin.site.register(Venta)
admin.site.register(Detalle_venta)