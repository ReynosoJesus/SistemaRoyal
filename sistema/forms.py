from django import forms
class Regform(forms.Form):
    usuario = forms.CharField(max_length=100)
    contraseña = forms.CharField(max_length=100)