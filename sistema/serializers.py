# serializers.py
from rest_framework import serializers  # This is important
from .models import Alumno,Libro,Certificado


class AlumnoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alumno
        fields = ('id', 'nombre', 'apellido', 'correo', 'fecha_nacimiento', 'telefono',
                  'direccion', 'ciudad', 'codigo_postal','estado','pais','contrasena','primerinicio')  # esto es lo que va a retornar esta cosa

class LibroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Libro
        fields = ('id', 'idioma', 'nivel', 'precio', 'restantes')

class CertificadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificado
        fields = ('id', 'id_alumno', 'id_grupo', 'archivo')
