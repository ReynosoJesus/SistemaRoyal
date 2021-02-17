from django.db import models

# Create your models here.

class Alumno(models.Model):
    nombre = models.CharField(max_length=200)
    apellido = models.CharField(max_length=200)
    correo = models.CharField(max_length=200)
    fecha_nacimiento = models.DateField()
    fecha_inscripcion = models.DateField()
    telefono = models.CharField(max_length=10)
    direccion = models.CharField(max_length=200)
    ciudad = models.CharField(max_length=200)
    codigo_postal = models.CharField(max_length=200)
    estado = models.CharField(max_length=200)
    pais = models.CharField(max_length=200)
    id_promocion = models.IntegerField()
    como_se_entero = models.CharField(max_length=200)
    anotaciones = models.CharField(max_length=500)
    #contrasena = models.CharField(max_length=40,default='12345')
    primerinicio = models.BooleanField(default=True)
    activo = models.BooleanField(default=True)
    usuarioreg = models.CharField(max_length=200)
    usuarioultmod = models.CharField(max_length=200)
    fechareg = models.DateField(auto_now_add=True)
    fechaultmod = models.DateField(auto_now=True)

class Docente(models.Model):
    nombre = models.CharField(max_length=200)
    apellido = models.CharField(max_length=200)
    correo = models.EmailField()
    fecha_nacimiento = models.DateField()
    fecha_inicio = models.DateField()
    telefono = models.CharField(max_length=200)
    direccion = models.CharField(max_length=200)
    ciudad = models.CharField(max_length=200)
    codigopostal = models.CharField(max_length=200)
    estado = models.CharField(max_length=200)
    pais = models.CharField(max_length=200)
    curp = models.CharField(max_length=200)
    rfc = models.CharField(max_length=200)
    activo = models.BooleanField(default=True)
    usuarioreg = models.CharField(max_length=200)
    usuarioultmod = models.CharField(max_length=200)
    fechareg = models.DateField(auto_now_add=True)
    fechaultmod = models.DateField(auto_now=True)

class Certificado(models.Model):
    id_curso = models.IntegerField()
    id_alumno = models.IntegerField()
    imagen = models.CharField(max_length=500)
    usuarioreg = models.CharField(max_length=200)
    usuarioultmod = models.CharField(max_length=200)
    fechareg = models.DateField()
    fechaultmod = models.DateField()

#tipo de registro: 1-pago alumno 2-pago docente 3-pago de algo en la tienda
#id de registro: id del alumno o del docente al que se le registra el pago
class Pago(models.Model):
    id_registro = models.IntegerField()
    tipo_registro = models.IntegerField()
    tipo_pago = models.CharField(max_length=200)
    metodo_pago = models.CharField(max_length=200)
    fechaPago = models.DateField(blank=True, null=True)
    promocion = models.IntegerField(blank=True, null=True)
    referencia = models.CharField(max_length=200, blank=True, null=True)
    cantidad = models.FloatField()
    usuarioreg = models.CharField(max_length=200)
    usuarioultmod = models.CharField(max_length=200)
    fechareg = models.DateField(auto_now_add=True)
    fechaultmod = models.DateField(auto_now=True)

#tipo de adeudo: 1-adeudo de reinscripcion o curso 2-adeudo de tienda
#id de registro: id del pago relacionado con el adeudo
class Adeudos(models.Model):
    id_registro = models.IntegerField()
    id_pago = models.IntegerField()
    tipo_adeudo = models.IntegerField()
    cantidad_adeudo = models.FloatField()
    activo = models.BooleanField(default=True)
    fechaProxima = models.DateField(blank=True, null=True)
    fecha_liquidacion = models.DateField(blank=True, null=True)
    usuarioreg = models.CharField(max_length=200)
    usuarioultmod = models.CharField(max_length=200)
    fechareg = models.DateField(auto_now_add=True)
    fechaultmod = models.DateField(auto_now=True)

class Grupo(models.Model):
    id_curso = models.IntegerField()
    id_docente = models.IntegerField()
    nombre = models.CharField(max_length=200)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    periodo = models.DateField()
    activo = models.BooleanField(default=True)
    promo_ofertada = models.BooleanField()
    alumnos_adeudos = models.BooleanField()
    tipo_grupo = models.CharField(max_length=200)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    usuarioreg = models.CharField(max_length=200)
    usuarioultmod = models.CharField(max_length=200)
    fechareg = models.DateField(auto_now_add=True)
    fechaultmod = models.DateField(auto_now=True)

class Aula(models.Model):
    nombre_aula = models.CharField(max_length=200)
    cantidad_sillas = models.IntegerField()
    cantidad_mesas = models.IntegerField()
    pantalla = models.BooleanField(default=False)
    ventanas = models.BooleanField(default=False)
    pintarron = models.BooleanField(default=False)
    aula_silenciada = models.BooleanField(default=False)
    capacidad = models.IntegerField()
    ventilacion = models.CharField(max_length=200) #ventilador, aire acondicionado.
    anotaciones = models.CharField(max_length=500, default="")
    activa = models.BooleanField(default=True)
    usuarioreg = models.CharField(max_length=200)
    usuarioultmod = models.CharField(max_length=200)
    fechareg = models.DateField(auto_now_add=True)
    fechaultmod = models.DateField(auto_now=True)

class Curso(models.Model):
    nombre = models.CharField(max_length=200)
    costo = models.FloatField()
    nivel = models.IntegerField()
    descripcion = models.CharField(max_length=500)
    activo = models.BooleanField(default=True)
    usuarioreg = models.CharField(max_length=200)
    usuarioultmod = models.CharField(max_length=200)
    fechareg = models.DateField(auto_now_add=True)
    fechaultmod = models.DateField(auto_now=True)

class Promocion(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.CharField(max_length=500)
    porcentaje = models.IntegerField()
    activa = models.BooleanField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    usuarioreg = models.CharField(max_length=200)
    usuarioultmod = models.CharField(max_length=200)
    fechareg = models.DateField(auto_now_add=True)
    fechaultmod = models.DateField(auto_now=True)

class Libro(models.Model):
    nombre = models.CharField(max_length=200)
    idioma = models.CharField(max_length=200)
    nivel = models.IntegerField()
    precio = models.FloatField()
    cantidad = models.IntegerField()
    fecha_inv = models.DateField()
    vendidos = models.IntegerField()
    restantes = models.IntegerField()
    agregados = models.IntegerField()
    total_en_venta = models.FloatField()
    anotaciones = models.CharField(max_length=500)
    usuarioreg = models.CharField(max_length=200)
    usuarioultmod = models.CharField(max_length=200)
    fechareg = models.DateField(auto_now_add=True)
    fechaultmod = models.DateField(auto_now=True)


# tablas relacionales
# cambiar nombre a rel_alu_grupo
class rel_alu_doc_grupo(models.Model):
    id_alumno = models.IntegerField()
    id_grupo = models.IntegerField()
    usuarioreg = models.CharField(max_length=200)
    usuarioultmod = models.CharField(max_length=200)
    fechareg = models.DateField(auto_now_add=True)
    fechaultmod = models.DateField(auto_now=True)

class rel_aula_grupo(models.Model):
    id_aula = models.IntegerField()
    id_grupo = models.IntegerField()
    usuarioreg = models.CharField(max_length=200)
    usuarioultmod = models.CharField(max_length=200)
    fechareg = models.DateField(auto_now_add=True)
    fechaultmod = models.DateField(auto_now=True)

# tablas venta de productos


class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    precio = models.FloatField()
    descripcion = models.CharField(max_length=200)
    inventario = models.IntegerField()
    activo = models.BooleanField()
    usuarioreg = models.CharField(max_length=200)
    usuarioultmod = models.CharField(max_length=200)
    fechareg = models.DateField(auto_now_add=True)
    fechaultmod = models.DateField(auto_now=True)

class Venta(models.Model):
    id_cliente = models.IntegerField()
    total = models.FloatField()
    cantPagada = models.IntegerField()
    usuarioreg = models.CharField(max_length=200)
    usuarioultmod = models.CharField(max_length=200)
    fechareg = models.DateField(auto_now_add=True)
    fechaultmod = models.DateField(auto_now=True)


class Detalle_venta(models.Model):
    id_venta = models.IntegerField()
    tipoProducto = models.CharField(max_length=200)
    id_producto = models.IntegerField()
    cantidad = models.IntegerField()
    monto = models.FloatField()
    usuarioreg = models.CharField(max_length=200)
    usuarioultmod = models.CharField(max_length=200)
    fechareg = models.DateField(auto_now_add=True)
    fechaultmod = models.DateField(auto_now=True)

#fechareg=fecha apertura de caja
class Caja(models.Model):
    cantidad = models.FloatField()
    activa = models.BooleanField()
    usuarioreg = models.CharField(max_length=200)
    usuarioultmod = models.CharField(max_length=200)
    fechareg = models.DateField(auto_now_add=True)
    fechaultmod = models.DateField(auto_now=True)


class CajaHelp(models.Model):    
    fechaultcaja= models.DateField()

class RegistroCaja(models.Model): 
    idMovimiento = models.AutoField(primary_key = True)
    tipo = models.CharField(max_length=200) #ingreso/egreso
    monto = models.FloatField()
    motivo = models.CharField(max_length=200) #venta, pago por alumno, pago a docente
    id_venta = models.IntegerField(null=True)
    usuarioreg = models.CharField(max_length=200)
    usuarioultmod = models.CharField(max_length=200)
    fechareg = models.DateField(auto_now_add=True)
    fechaultmod = models.DateField(auto_now=True)