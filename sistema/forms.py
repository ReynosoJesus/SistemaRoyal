from django import forms

class Regform(forms.Form):
    usuario = forms.CharField(max_length=100)
    contraseña = forms.CharField(max_length=100)

class UploadFileForm(forms.Form):
    id_alumno = forms.IntegerField()
    id_grupo = forms.IntegerField()
    title = forms.CharField(max_length=50)
    file = forms.FileField()