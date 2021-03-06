# Generated by Django 3.1 on 2021-03-09 23:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Adeudos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_registro', models.IntegerField()),
                ('id_pago', models.IntegerField()),
                ('tipo_adeudo', models.IntegerField()),
                ('cantidad_adeudo', models.FloatField()),
                ('activo', models.BooleanField(default=True)),
                ('fechaProxima', models.DateField(blank=True, null=True)),
                ('fecha_liquidacion', models.DateField(blank=True, null=True)),
                ('usuarioreg', models.CharField(max_length=200)),
                ('usuarioultmod', models.CharField(max_length=200)),
                ('fechareg', models.DateField(auto_now_add=True)),
                ('fechaultmod', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Alumno',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
                ('apellido', models.CharField(max_length=200)),
                ('correo', models.CharField(max_length=200)),
                ('fecha_nacimiento', models.DateField()),
                ('fecha_inscripcion', models.DateField()),
                ('telefono', models.CharField(max_length=10)),
                ('direccion', models.CharField(max_length=200)),
                ('ciudad', models.CharField(max_length=200)),
                ('codigo_postal', models.CharField(max_length=200)),
                ('estado', models.CharField(max_length=200)),
                ('pais', models.CharField(max_length=200)),
                ('id_promocion', models.IntegerField()),
                ('como_se_entero', models.CharField(max_length=200)),
                ('anotaciones', models.CharField(max_length=500)),
                ('contrasena', models.CharField(default='12345', max_length=40)),
                ('primerinicio', models.BooleanField(default=True)),
                ('activo', models.BooleanField(default=True)),
                ('usuarioreg', models.CharField(max_length=200)),
                ('usuarioultmod', models.CharField(max_length=200)),
                ('fechareg', models.DateField(auto_now_add=True)),
                ('fechaultmod', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Aula',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_aula', models.CharField(max_length=200)),
                ('cantidad_sillas', models.IntegerField()),
                ('cantidad_mesas', models.IntegerField()),
                ('pantalla', models.BooleanField(default=False)),
                ('ventanas', models.BooleanField(default=False)),
                ('pintarron', models.BooleanField(default=False)),
                ('aula_silenciada', models.BooleanField(default=False)),
                ('capacidad', models.IntegerField()),
                ('ventilacion', models.CharField(max_length=200)),
                ('anotaciones', models.CharField(default='', max_length=500)),
                ('activa', models.BooleanField(default=True)),
                ('usuarioreg', models.CharField(max_length=200)),
                ('usuarioultmod', models.CharField(max_length=200)),
                ('fechareg', models.DateField(auto_now_add=True)),
                ('fechaultmod', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Caja',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.FloatField()),
                ('activa', models.BooleanField()),
                ('usuarioreg', models.CharField(max_length=200)),
                ('usuarioultmod', models.CharField(max_length=200)),
                ('fechareg', models.DateField(auto_now_add=True)),
                ('fechaultmod', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='CajaHelp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fechaultcaja', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Certificado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_grupo', models.IntegerField()),
                ('id_alumno', models.IntegerField()),
                ('archivo', models.FileField(blank=True, null=True, upload_to='media/certificados')),
                ('usuarioreg', models.CharField(max_length=200)),
                ('usuarioultmod', models.CharField(max_length=200)),
                ('fechareg', models.DateField()),
                ('fechaultmod', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Curso',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
                ('costo', models.FloatField()),
                ('nivel', models.IntegerField()),
                ('descripcion', models.CharField(max_length=500)),
                ('activo', models.BooleanField(default=True)),
                ('usuarioreg', models.CharField(max_length=200)),
                ('usuarioultmod', models.CharField(max_length=200)),
                ('fechareg', models.DateField(auto_now_add=True)),
                ('fechaultmod', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Detalle_venta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_venta', models.IntegerField()),
                ('tipoProducto', models.CharField(max_length=200)),
                ('id_producto', models.IntegerField()),
                ('cantidad', models.IntegerField()),
                ('monto', models.FloatField()),
                ('usuarioreg', models.CharField(max_length=200)),
                ('usuarioultmod', models.CharField(max_length=200)),
                ('fechareg', models.DateField(auto_now_add=True)),
                ('fechaultmod', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Docente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
                ('apellido', models.CharField(max_length=200)),
                ('correo', models.EmailField(max_length=254)),
                ('fecha_nacimiento', models.DateField()),
                ('fecha_inicio', models.DateField()),
                ('telefono', models.CharField(max_length=200)),
                ('direccion', models.CharField(max_length=200)),
                ('ciudad', models.CharField(max_length=200)),
                ('codigopostal', models.CharField(max_length=200)),
                ('estado', models.CharField(max_length=200)),
                ('pais', models.CharField(max_length=200)),
                ('curp', models.CharField(max_length=200)),
                ('rfc', models.CharField(max_length=200)),
                ('activo', models.BooleanField(default=True)),
                ('usuarioreg', models.CharField(max_length=200)),
                ('usuarioultmod', models.CharField(max_length=200)),
                ('fechareg', models.DateField(auto_now_add=True)),
                ('fechaultmod', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Grupo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_curso', models.IntegerField()),
                ('id_docente', models.IntegerField()),
                ('nombre', models.CharField(max_length=200)),
                ('fecha_inicio', models.DateField()),
                ('fecha_fin', models.DateField()),
                ('periodo', models.DateField()),
                ('activo', models.BooleanField(default=True)),
                ('promo_ofertada', models.BooleanField()),
                ('alumnos_adeudos', models.BooleanField()),
                ('tipo_grupo', models.CharField(max_length=200)),
                ('hora_inicio', models.TimeField()),
                ('hora_fin', models.TimeField()),
                ('usuarioreg', models.CharField(max_length=200)),
                ('usuarioultmod', models.CharField(max_length=200)),
                ('fechareg', models.DateField(auto_now_add=True)),
                ('fechaultmod', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Libro',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
                ('idioma', models.CharField(max_length=200)),
                ('nivel', models.IntegerField()),
                ('precio', models.FloatField()),
                ('cantidad', models.IntegerField()),
                ('fecha_inv', models.DateField()),
                ('vendidos', models.IntegerField()),
                ('restantes', models.IntegerField()),
                ('agregados', models.IntegerField()),
                ('total_en_venta', models.FloatField()),
                ('anotaciones', models.CharField(max_length=500)),
                ('usuarioreg', models.CharField(max_length=200)),
                ('usuarioultmod', models.CharField(max_length=200)),
                ('fechareg', models.DateField(auto_now_add=True)),
                ('fechaultmod', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Pago',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_registro', models.IntegerField()),
                ('tipo_registro', models.IntegerField()),
                ('tipo_pago', models.CharField(max_length=200)),
                ('metodo_pago', models.CharField(max_length=200)),
                ('fechaPago', models.DateField(blank=True, null=True)),
                ('promocion', models.IntegerField(blank=True, null=True)),
                ('referencia', models.CharField(blank=True, max_length=200, null=True)),
                ('cantidad', models.FloatField()),
                ('usuarioreg', models.CharField(max_length=200)),
                ('usuarioultmod', models.CharField(max_length=200)),
                ('fechareg', models.DateField(auto_now_add=True)),
                ('fechaultmod', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
                ('precio', models.FloatField()),
                ('descripcion', models.CharField(max_length=200)),
                ('inventario', models.IntegerField()),
                ('activo', models.BooleanField()),
                ('usuarioreg', models.CharField(max_length=200)),
                ('usuarioultmod', models.CharField(max_length=200)),
                ('fechareg', models.DateField(auto_now_add=True)),
                ('fechaultmod', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Promocion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
                ('descripcion', models.CharField(max_length=500)),
                ('porcentaje', models.IntegerField()),
                ('activa', models.BooleanField()),
                ('fecha_inicio', models.DateField()),
                ('fecha_fin', models.DateField()),
                ('usuarioreg', models.CharField(max_length=200)),
                ('usuarioultmod', models.CharField(max_length=200)),
                ('fechareg', models.DateField(auto_now_add=True)),
                ('fechaultmod', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='RegistroCaja',
            fields=[
                ('idMovimiento', models.AutoField(primary_key=True, serialize=False)),
                ('tipo', models.CharField(max_length=200)),
                ('monto', models.FloatField()),
                ('motivo', models.CharField(max_length=200)),
                ('id_venta', models.IntegerField(null=True)),
                ('usuarioreg', models.CharField(max_length=200)),
                ('usuarioultmod', models.CharField(max_length=200)),
                ('fechareg', models.DateField(auto_now_add=True)),
                ('fechaultmod', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='rel_alu_doc_grupo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_alumno', models.IntegerField()),
                ('id_grupo', models.IntegerField()),
                ('usuarioreg', models.CharField(max_length=200)),
                ('usuarioultmod', models.CharField(max_length=200)),
                ('fechareg', models.DateField(auto_now_add=True)),
                ('fechaultmod', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='rel_aula_grupo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_aula', models.IntegerField()),
                ('id_grupo', models.IntegerField()),
                ('usuarioreg', models.CharField(max_length=200)),
                ('usuarioultmod', models.CharField(max_length=200)),
                ('fechareg', models.DateField(auto_now_add=True)),
                ('fechaultmod', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Venta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_cliente', models.IntegerField()),
                ('total', models.FloatField()),
                ('cantPagada', models.IntegerField()),
                ('usuarioreg', models.CharField(max_length=200)),
                ('usuarioultmod', models.CharField(max_length=200)),
                ('fechareg', models.DateField(auto_now_add=True)),
                ('fechaultmod', models.DateField(auto_now=True)),
            ],
        ),
    ]
