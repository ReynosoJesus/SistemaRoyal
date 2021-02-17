from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from .forms import Regform
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .utils import render_to_pdf
from datetime import date
import base64
import datetime
import operator
import json
import locale

locale.setlocale(locale.LC_TIME, '')
def inicio(request):
    if not CajaHelp.objects.all():
        CajaHelp(fechaultcaja=datetime.datetime.now()).save()
    else:
        help = CajaHelp.objects.last()
        CajaHelp.objects.filter(pk=help.id).update(
            fechaultcaja=datetime.datetime.now())
    if request.user.is_authenticated:
        return render(request, 'base.html', {})
    else:
        if request.method == 'POST':
            if 'inicio' in request.POST:
                usuario = request.POST['user']
                password = request.POST['password']
                user = authenticate(
                    request, username=usuario, password=password)
                if user is not None:
                    login(request, user)
                    help = CajaHelp.objects.first()
                    cajas = Caja.objects.all()
                    if not cajas:
                        return HttpResponseRedirect("/caja/")
                    else:
                        caja = cajas.last()
                        if caja.fechareg != help.fechaultcaja:
                            return redirect('caja')
                        else:
                            return redirect('home')
                else:
                    messages.info(request,"usuario o contraseña incorrectos")            
                    return render(request, 'inicio.html', {})
    return render(request, 'inicio.html', {})

def logoutUser(request):
    logout(request)
    return redirect('inicio')

@login_required(login_url='inicio')
def base(request):
    return render(request, 'base.html', {})

@login_required(login_url='inicio')
def consultar_a(request):
    alumnos = Alumno.objects.all()
    grupos = Grupo.objects.all()
    aulas = Aula.objects.all()
    cursos = Curso.objects.all()
    docentes = Docente.objects.all()
    promociones = Promocion.objects.all()
    rel = rel_alu_doc_grupo.objects.all()
    for x in alumnos:
        x.fecha_inscripcion = x.fecha_inscripcion.strftime("%d-%m-%Y")
    Context = {
        'Alumnos': alumnos,
        'Aulas': aulas,
        'Cursos': cursos,
        'Docentes': docentes,
        'Grupos': grupos,
        'Promociones': promociones,
        'Rel': rel
    }
    if request.method == 'POST':
        if 'registrar' in request.POST:
            nombre = request.POST['Rnombre']
            apellidos = request.POST['Rapellido']
            correo = request.POST['Rcorreo']
            fecha_nac = request.POST['Rfecha_nac']
            fecha_ins = request.POST['Rfecha_ins']
            telefono = request.POST['Rnumtel']
            direccion = request.POST['Rdireccion']
            ciudad = request.POST['Rciudad']
            codigopostal = request.POST['Rcodigopostal']
            estado = request.POST['Restado']
            pais = request.POST['Rpais']
            grupo = request.POST['Rgrupo']
            promocion = request.POST['Rpromo']
            enterado = request.POST['Renterado']
            anotaciones = request.POST['Ranotaciones']
            usuario = request.user.username
            grupo_f = Grupo.objects.get(pk=grupo)
            docente_f = Docente.objects.get(pk=grupo_f.id_docente)
            nuevo_alumno = Alumno(nombre=nombre, apellido=apellidos, correo=correo, fecha_nacimiento=fecha_nac, fecha_inscripcion=fecha_ins, telefono=telefono, direccion=direccion, ciudad=ciudad,
                                  codigo_postal=codigopostal, estado=estado, pais=pais, id_promocion=promocion, como_se_entero=enterado, anotaciones=anotaciones, usuarioreg=usuario, usuarioultmod=usuario)
            nuevo_alumno.save()
            nueva_rel = rel_alu_doc_grupo(usuarioultmod=usuario, usuarioreg=usuario,id_alumno=nuevo_alumno.pk, id_grupo=grupo_f.pk)
            nueva_rel.save()
            return HttpResponseRedirect("/consulta_a/")
        elif 'modificar' in request.POST:
            idmod = request.POST['modificar']
            nombre = request.POST['Mnombre']
            apellidos = request.POST['Mapellido']
            correo = request.POST['Mcorreo']
            fecha_nac = request.POST['Mfecha_nac']
            fecha_ins = request.POST['Mfecha_ins']
            telefono = request.POST['Mnumtel']
            direccion = request.POST['Mdireccion']
            ciudad = request.POST['Mciudad']
            codigopostal = request.POST['Mcodigopostal']
            estado = request.POST['Mestado']
            pais = request.POST['Mpais']
            promocion = request.POST['Mpromo']
            enterado = request.POST['Menterado']
            anotaciones = request.POST['Manotaciones']
            usuario = request.user.username
            Alumno.objects.filter(pk=idmod).update(nombre=nombre, apellido=apellidos, correo=correo, fecha_nacimiento=fecha_nac, fecha_inscripcion=fecha_ins, telefono=telefono, direccion=direccion, ciudad=ciudad,
                                                   codigo_postal=codigopostal, estado=estado, pais=pais, id_promocion=promocion, como_se_entero=enterado, anotaciones=anotaciones, usuarioultmod=usuario, fechaultmod=datetime.datetime.now())
            return HttpResponseRedirect("/consulta_a/")
        elif 'eliminar' in request.POST:
            iddel = request.POST['eliminar']
            usuario = request.user.username
            Alumno.objects.filter(pk=iddel).update(activo=False,fechaultmod=datetime.datetime.now(),usuarioultmod=usuario)
            return HttpResponseRedirect("/consulta_a/")
        elif 'reactivar' in request.POST:
            idreac = request.POST['reactivar']
            usuario = request.user.username
            Alumno.objects.filter(pk=idreac).update(activo=True,fechaultmod=datetime.datetime.now(),usuarioultmod=usuario)
            return HttpResponseRedirect("/consulta_a/")
    return render(request, 'consultar_alumnos.html', Context)


def modalAlumnos(request, alumno=None):
    AlumnoF = Alumno.objects.get(pk=alumno)
    AlumnoF.fecha_nacimiento = AlumnoF.fecha_nacimiento.strftime("%Y-%m-%d")
    AlumnoF.fecha_inscripcion = AlumnoF.fecha_inscripcion.strftime("%Y-%m-%d")
    promociones = Promocion.objects.all()
    rel = rel_alu_doc_grupo.objects.filter(id_alumno=alumno)
    adeudos = Adeudos.objects.filter(id_registro=alumno)
    grupos = Grupo.objects.all()
    aulas = Aula.objects.all()
    cursos = Curso.objects.all()
    redes = "redes"
    volantes = "volantes"
    carteles = "carteles"
    Context = {
        'AlumnoF': AlumnoF,
        'Promociones': promociones,
        'redes': redes,
        'volantes': volantes,
        'carteles': carteles,
        'Rel': rel,
        'Grupos': grupos,
        'Aulas': aulas,
        'Cursos': cursos,
        'Adeudos': adeudos
    }
    return render(request, 'modales.html', Context)

@login_required(login_url='inicio')
def consultar_d(request):
    docentes = Docente.objects.all()
    if request.method == 'POST':
        if 'registrar' in request.POST:
            nombre = request.POST['RnombresD']
            apellidos = request.POST['RapellidosD']
            correo = request.POST['RcorreoD']
            fecha_nac = request.POST['RfechanacD']
            fecha_ini = request.POST['Rfechaini']
            telefono = request.POST['RnumerotelD']
            direccion = request.POST['RdireccionD']
            ciudad = request.POST['RciudadD']
            cp = request.POST['RcodpostalD']
            estado = request.POST['RestadoD']
            pais = request.POST['RpaisD']
            curp = request.POST['RcurpD']
            rfc = request.POST['RrfcD']
            usuario = request.user.username
            docente_nuevo = Docente(nombre=nombre, apellido=apellidos, correo=correo, fecha_nacimiento=fecha_nac, telefono=telefono, direccion=direccion, activo=True,
                                    ciudad=ciudad, estado=estado, pais=pais, usuarioreg=usuario, usuarioultmod=usuario, fecha_inicio=fecha_ini, codigopostal=cp, curp=curp, rfc=rfc)
            docente_nuevo.save()
            return HttpResponseRedirect("/consulta_d/")
        elif 'modificar' in request.POST:
            idmod = request.POST['modificar']
            nombre = request.POST['MnombresD']
            apellidos = request.POST['MapellidosD']
            correo = request.POST['McorreoD']
            fecha_nac = request.POST['MfechanacD']
            fecha_ini = request.POST['Mfechaini']
            telefono = request.POST['MnumerotelD']
            direccion = request.POST['MdireccionD']
            ciudad = request.POST['MciudadD']
            cp = request.POST['McodpostalD']
            estado = request.POST['MestadoD']
            pais = request.POST['MpaisD']
            curp = request.POST['McurpD']
            rfc = request.POST['MrfcD']
            usuario = request.user.username
            Docente.objects.filter(pk=idmod).update(nombre=nombre, apellido=apellidos, correo=correo, fecha_nacimiento=fecha_nac, telefono=telefono, direccion=direccion,
                                                    usuarioultmod=usuario, fechaultmod=datetime.datetime.now(), ciudad=ciudad, estado=estado, pais=pais, fecha_inicio=fecha_ini, codigopostal=cp, curp=curp, rfc=rfc)
            return HttpResponseRedirect("/consulta_d/")
        elif 'eliminar' in request.POST:
            iddel = request.POST['eliminar']
            usuario = request.user.username
            Docente.objects.filter(pk=iddel).update(activo=False,fechaultmod=datetime.datetime.now(),usuarioultmod=usuario)
            return HttpResponseRedirect("/consulta_d/")
        elif 'reactivar' in request.POST:
            idreac = request.POST['reactivar']
            usuario = request.user.username
            Docente.objects.filter(pk=idreac).update(activo=True,fechaultmod=datetime.datetime.now(),usuarioultmod=usuario)
            return HttpResponseRedirect("/consulta_d/")
    return render(request, 'consultar_docente.html', {'Docentes': docentes})


def modalDocentes(request, id=None):
    DocenteF = Docente.objects.get(pk=id)
    DocenteF.fecha_inicio = DocenteF.fecha_inicio.strftime("%Y-%m-%d")
    DocenteF.fecha_nacimiento = DocenteF.fecha_nacimiento.strftime("%Y-%m-%d")
    return render(request, 'modales.html', {'DocenteF': DocenteF})

@login_required(login_url='inicio')
def certificados(request):
    Alumnos = Alumno.objects.all()
    Context = {
        'Alumnos':Alumnos
    }
    if request.method == 'POST':
        if 'certificar' in request.POST:    
            nombre=request.POST['Rnombre']
            nombre=nombre.upper()
            apellido=request.POST['Rapellido']
            apellido=apellido.upper()
            curso=request.POST['Rcurso']
            curso1=curso.split('-')
            Cnombre=curso1[0].upper()
            Cnivel=curso1[1]
            fecha= date.today().strftime("%w %B, %Y").upper()
            horas=request.POST['Rhoras']
            bandera=request.FILES["Rbandera"].read()
            image_data = base64.b64encode(bandera).decode('utf-8')
            Context = {
                'Nombre':nombre,
                'Apellido':apellido,
                'Fecha':fecha,
                'Curso':Cnombre,
                'Nivel':Cnivel,
                'Horas':horas,
                'Bandera':image_data
            }
            pdf = render_to_pdf('invoice.html',Context)
            return HttpResponse(pdf, content_type='application/pdf')
    return render(request, 'certificados.html', Context)

def modalcertificados(request, id_alumno=None):
    #solo para consulta dinamica de los cursos de cada alumno
    if id_alumno is not None:
        print("entro",id_alumno)
        # este if ayuda a la consulta dinamica de los grupos y adeudos
        rel = rel_alu_doc_grupo.objects.filter(id_alumno=id_alumno)
        grupos = Grupo.objects.all()
        cursos = Curso.objects.all()
        aulas = Aula.objects.all()
        Alumno_f=Alumno.objects.get(pk=id_alumno)
        print(Alumno_f.nombre)
        Context = {
            'Grupos': grupos,
            'Rel': rel,
            'Cursos': cursos,
            'Aulas': aulas,
            'Alumno_f':Alumno_f
        }
        data = {'rendered_table': render_to_string(
            'combos_certificados.html', context=Context)}
        return JsonResponse(data)


@login_required(login_url='inicio')
def curso(request):
    cursos = Curso.objects.all()
    if request.method == 'POST':
        if 'registrar' in request.POST:
            nombre = request.POST['Rnombrecurso']
            nivel = request.POST['Rnivel']
            costo = request.POST['Rcosto']
            descripcion = request.POST['Rdescurso']
            usuario = request.user.username
            Curso_nuevo = Curso(nombre=nombre, costo=costo, nivel=nivel, activo=True,
                                descripcion=descripcion, usuarioreg=usuario, usuarioultmod=usuario)
            Curso_nuevo.save()
            return HttpResponseRedirect("/curso/")
        elif 'modificar' in request.POST:
            idmod = request.POST['modificar']
            nombre = request.POST['Mnombrecurso']
            nivel = request.POST['Mnivel']
            costo = request.POST['Mcosto']
            descripcion = request.POST['Mdescurso']
            usuario = request.user.username
            Curso.objects.filter(pk=idmod).update(
                nombre=nombre, nivel=nivel, costo=costo, descripcion=descripcion, usuarioultmod=usuario, fechaultmod=datetime.datetime.now())
            return HttpResponseRedirect("/curso/")
        elif 'eliminar' in request.POST:
            iddel = request.POST['eliminar']
            usuario = request.user.username
            Curso.objects.filter(pk=iddel).update(activo=False,fechaultmod=datetime.datetime.now(),usuarioultmod=usuario)
            return HttpResponseRedirect("/curso/")
    return render(request, 'curso.html', {"Curso": cursos})


def modalCursos(request, id=None):
    CursoF = Curso.objects.get(pk=id)
    return render(request, 'modales.html', {'CursoF': CursoF})

@login_required(login_url='inicio')
def aula(request):
    aulas = Aula.objects.all()
    if request.method == 'POST':
        if 'registrar' in request.POST:
            nombre = request.POST['RnAula']
            num_sillas = request.POST['Rnumsillas']
            num_mesas = request.POST['Rnummesas']
            capacidad = request.POST['Rnumalumnos']
            ventilacion = request.POST.get('Rventilacion', '')
            ventanas = request.POST.get('Rventanas', '')
            pintarron = request.POST.get('Rpintarron', '')
            aula_silenciada = request.POST.get('Rsilencio', '')
            pantalla = request.POST.get('Rpantalla', '')
            anotaciones = request.POST['Ranotaciones']
            usuario = request.user.username
            if(ventilacion == ''):
                ventilacion=False 
            else:
                ventilacion=True
            if(ventanas == ''):
                ventanas=False 
            else:
                ventanas=True
            if(pintarron == ''):
                pintarron=False 
            else:
                pintarron=True
            if(aula_silenciada == ''):
                aula_silenciada=False 
            else:
                aula_silenciada=True
            if(pantalla == ''):
                pantalla=False 
            else:
                pantalla=True
            aula_nueva = Aula(nombre_aula=nombre,cantidad_sillas=num_sillas,cantidad_mesas=num_mesas,ventilacion=ventilacion,capacidad=capacidad,
                ventanas=ventanas,anotaciones=anotaciones,pantalla=pantalla,pintarron=pintarron,aula_silenciada=aula_silenciada,usuarioreg=usuario, usuarioultmod=usuario)
            aula_nueva.save()
            return HttpResponseRedirect("/aula/")
        elif 'modificar' in request.POST:
            idmod = request.POST['modificar']
            nombre = request.POST['MnAula']
            num_sillas = request.POST['Mnumsillas']
            num_mesas = request.POST['Mnummesas']
            capacidad = request.POST['Mnumalumnos']
            ventilacion = request.POST.get('Mventilacion', '')
            ventanas = request.POST.get('Mventanas', '')
            pintarron = request.POST.get('Mpintarron', '')
            pantalla = request.POST.get('Mpantalla', '')
            aula_silenciada = request.POST.get('Msilencio', '')
            anotaciones = request.POST['Manotaciones']
            usuario = request.user.username
            if(ventilacion == ''):
                ventilacion=False 
            else:
                ventilacion=True
            if(ventanas == ''):
                ventanas=False 
            else:
                ventanas=True
            if(pintarron == ''):
                pintarron=False 
            else:
                pintarron=True
            if(aula_silenciada == ''):
                aula_silenciada=False 
            else:
                aula_silenciada=True
            if(pantalla == ''):
                pantalla=False 
            else:
                pantalla=True
            Aula.objects.filter(pk=idmod).update(nombre_aula=nombre,cantidad_sillas=num_sillas,cantidad_mesas=num_mesas,ventilacion=ventilacion,capacidad=capacidad,
                ventanas=ventanas,pantalla=pantalla,anotaciones=anotaciones,pintarron=pintarron,aula_silenciada=aula_silenciada,usuarioreg=usuario,usuarioultmod=usuario, fechaultmod=datetime.datetime.now())
            return HttpResponseRedirect("/aula/")
        elif 'eliminar' in request.POST:
            iddel = request.POST['eliminar']
            usuario = request.user.username
            Aula.objects.filter(pk=iddel).update(activa=False,usuarioultmod=usuario, fechaultmod=datetime.datetime.now())
            return HttpResponseRedirect("/aula/")
    return render(request, 'aula.html', {"Aulas": aulas})

def modalAulas(request, id=None):
    AulaF = Aula.objects.get(pk=id)
    return render(request, 'modales.html', {'AulaF': AulaF})

@login_required(login_url='inicio')
def promociones(request):
    Promociones = Promocion.objects.all()
    if request.method == 'POST':
        if 'registrar' in request.POST:
            nombre = request.POST['RnombreP']
            desc = request.POST['RdescripcionP']
            fecha_ini = request.POST['RfechainiP']
            fecha_fin = request.POST['RfechafinP']
            porcentaje = request.POST['RporcentajeP']
            usuario = request.user.username
            promo_nueva = Promocion(nombre=nombre, porcentaje=porcentaje, fecha_inicio=fecha_ini,
                                    fecha_fin=fecha_fin, descripcion=desc, usuarioreg=usuario, usuarioultmod=usuario, activa=True)
            promo_nueva.save()
            return HttpResponseRedirect("/promociones/")
        elif 'modificar' in request.POST:
            idmod = request.POST['modificar']
            nombre = request.POST['MnombreP']
            desc = request.POST['MdescripcionP']
            fecha_ini = request.POST['MfechainiP']
            fecha_fin = request.POST['MfechafinP']
            porcentaje = request.POST['MporcentajeP']
            activo = request.POST.get('MactivarP', '')
            usuario = request.user.username
            if(activo == ''):
                Promocion.objects.filter(pk=idmod).update(nombre=nombre, porcentaje=porcentaje, fecha_inicio=fecha_ini, fecha_fin=fecha_fin,
                                                          descripcion=desc, activa=False, usuarioultmod=usuario, fechaultmod=datetime.datetime.now())
                return HttpResponseRedirect("/promociones/")
            else:
                Promocion.objects.filter(pk=idmod).update(nombre=nombre, porcentaje=porcentaje, fecha_inicio=fecha_ini, fecha_fin=fecha_fin,
                                                          descripcion=desc, activa=True, usuarioultmod=usuario, fechaultmod=datetime.datetime.now())
                return HttpResponseRedirect("/promociones/")
        elif 'eliminar' in request.POST:
            iddel = request.POST['eliminar']
            usuario = request.user.username
            Promocion.objects.filter(pk=iddel).update(activa=False,usuarioultmod=usuario, fechaultmod=datetime.datetime.now())
            return HttpResponseRedirect("/promociones/")
    return render(request, 'promociones.html', {'Promociones': Promociones})


def modalpromociones(request, id=None):
    PromocionF = Promocion.objects.get(pk=id)
    PromocionF.fecha_inicio = PromocionF.fecha_inicio.strftime("%Y-%m-%d")
    PromocionF.fecha_fin = PromocionF.fecha_fin.strftime("%Y-%m-%d")
    return render(request, 'modales.html', {'PromocionF': PromocionF})

@login_required(login_url='inicio')
def grupos(request):
    aulas = Aula.objects.all()
    cursos = Curso.objects.all()
    docentes = Docente.objects.all()
    grupos = Grupo.objects.all()
    Context = {
        'Aulas': aulas,
        'Cursos': cursos,
        'Docentes': docentes,
        'Grupos': grupos
    }
    if request.method == 'POST':
        if 'registrar' in request.POST:
            nombre = request.POST['Rnombre']
            curso = request.POST['Rcurso']
            aula = request.POST['Raula']
            docente = request.POST['Rdocente']
            fecha_inicio = request.POST['Rfinicio']
            fecha_fin = request.POST['Rffin']
            hora_inicio = request.POST['Rhinicio']
            hora_fin = request.POST['Rhfin']
            periodo = request.POST['Rperiodo']
            periodo_final = periodo+"-01"
            tipo = request.POST['Rtipo']
            usuario = request.user.username
            grupo_nuevo = Grupo(nombre=nombre, id_curso=curso, id_docente=docente, usuarioreg=usuario, usuarioultmod=usuario,
                                fecha_inicio=fecha_inicio, fecha_fin=fecha_fin,hora_inicio=hora_inicio,hora_fin=hora_fin, periodo=periodo_final, promo_ofertada=False, alumnos_adeudos=False, tipo_grupo=tipo)
            grupo_nuevo.save()
            rel_nueva = rel_aula_grupo(usuarioreg=usuario,usuarioultmod=usuario,id_aula=aula,id_grupo=grupo_nuevo.pk)
            rel_nueva.save()
            return HttpResponseRedirect("/grupos/")
        elif 'modificar' in request.POST:
            idmod = request.POST['modificar']
            nombre = request.POST['Mnombre']
            curso = request.POST['Mcurso']
            aula = request.POST.get('Maula', '')
            docente = request.POST['Mdocente']
            fecha_inicio = request.POST['Mfinicio']
            fecha_fin = request.POST['Mffin']
            hora_inicio = request.POST['Mhinicio']
            hora_fin = request.POST['Mhfin']
            periodo = request.POST['Mperiodo']
            periodo_final = periodo+"-01"
            tipo = request.POST['Mtipo']
            usuario = request.user.username
            promocion = request.POST.get('Mpromocion', '')
            if(promocion == ''):
                promocion=False 
            else:
                promocion=True
            Grupo.objects.filter(pk=idmod).update(nombre=nombre, id_curso=curso, id_docente=docente, usuarioultmod=usuario, fechaultmod=datetime.datetime.now(),
                                                  fecha_inicio=fecha_inicio, fecha_fin=fecha_fin,hora_inicio=hora_inicio,hora_fin=hora_fin, periodo=periodo_final, promo_ofertada=promocion, tipo_grupo=tipo)
            return HttpResponseRedirect("/grupos/")
        elif 'eliminar' in request.POST:
            iddel = request.POST['eliminar']
            usuario = request.user.username
            Grupo.objects.filter(pk=iddel).update(activo=False,usuarioultmod=usuario,fechaultmod=datetime.datetime.now())
            return HttpResponseRedirect("/grupos/")
    return render(request, 'grupos.html', Context)


def modalgrupos(request, id=None):
    GrupoF = Grupo.objects.get(pk=id)
    Curso_f = Curso.objects.get(pk=GrupoF.id_curso)
    Docente_f = Docente.objects.get(pk=GrupoF.id_docente)
    aulas = Aula.objects.all()
    cursos = Curso.objects.all()
    docentes = Docente.objects.all()
    rel = rel_alu_doc_grupo.objects.filter(id_grupo=id)
    relA = rel_aula_grupo.objects.filter(id_grupo=id)
    adeudos = Adeudos.objects.filter(activo=True)
    Aulas_f =Aula.objects.all()
    for x in relA:
        Aulas_f = Aulas_f.exclude(pk=x.id_aula)
    for a in rel:
        adeudos.filter(id_registro=a.id_alumno)        
        if adeudos.count() > 0:
            GrupoF.alumnos_adeudos = True
            GrupoF.save()
        else:
            GrupoF.alumnos_adeudos = False
            GrupoF.save()
    Alumnos_f = Alumno.objects.all()
    for y in rel:
        Alumnos_f = Alumnos_f.exclude(pk=y.id_alumno)
    Alumnos = Alumno.objects.all()
    for x in Alumnos:
        x.fecha_inscripcion = x.fecha_inscripcion.strftime("%d-%m-%Y")
    for z in Alumnos_f:
        z.fecha_inscripcion = z.fecha_inscripcion.strftime("%d-%m-%Y")
    Linea = 'Linea'
    Presencial = 'Presencial'
    GrupoF.fecha_inicio = GrupoF.fecha_inicio.strftime("%Y-%m-%d")
    GrupoF.fecha_fin = GrupoF.fecha_fin.strftime("%Y-%m-%d")
    GrupoF.periodo = GrupoF.periodo.strftime("%Y-%m")
    GrupoF.hora_inicio = GrupoF.hora_inicio.strftime("%H:%M")
    GrupoF.hora_fin = GrupoF.hora_fin.strftime("%H:%M")
    Aulas = Aula.objects.all()
    Context = {
        'GrupoF': GrupoF,
        'Curso_f': Curso_f,
        'Docente_f': Docente_f,
        'Aulas': aulas,
        'Cursos': cursos,
        'Docentes': docentes,
        'Linea': Linea,
        'Presencial': Presencial,
        'Rel': rel,
        'RelA': relA,
        'Aulas': Aulas,
        'Aulas_f':Aulas_f,
        'Alumnos': Alumnos,
        'Alumnos_f': Alumnos_f
    }
    return render(request, 'modales.html', Context)


def moverAlumnos(request, id_alumno=None, id_grupo=None, movimiento=None):
    if request.is_ajax():
        GrupoF = Grupo.objects.get(pk=id_grupo)
        if movimiento == 1:
            rel_alu_doc_grupo.objects.filter(
                id_grupo=id_grupo, id_alumno=id_alumno).delete()
        elif movimiento == 2:
            usuario = 'reynoso'
            nueva_rel = rel_alu_doc_grupo(usuarioultmod=usuario, usuarioreg=usuario,id_alumno=id_alumno, id_grupo=id_grupo)
            nueva_rel.save()
        rel = rel_alu_doc_grupo.objects.filter(id_grupo=id_grupo)
        Alumnos_f = Alumno.objects.all()
        for y in rel:
            Alumnos_f = Alumnos_f.exclude(pk=y.id_alumno)
        Alumnos = Alumno.objects.all()
        for x in Alumnos:
            x.fecha_inscripcion = x.fecha_inscripcion.strftime("%d-%m-%Y")
        for z in Alumnos_f:
            z.fecha_inscripcion = z.fecha_inscripcion.strftime("%d-%m-%Y")
        Context = {
            'GrupoF': GrupoF,
            'Rel': rel,
            'Alumnos': Alumnos,
            'Alumnos_f': Alumnos_f
        }
        data = {'rendered_table': render_to_string(
            'tabla_grupos.html', context=Context)}
        return JsonResponse(data)

def moverAulas(request, id_aula=None, id_grupo=None, movimiento=None):
    if request.is_ajax():
        GrupoF = Grupo.objects.get(pk=id_grupo)
        if movimiento == 1:
            rel_aula_grupo.objects.filter(
                id_grupo=id_grupo, id_aula=id_aula).delete()
        elif movimiento == 2:
            usuario = 'reynoso'
            nueva_rel = rel_aula_grupo(usuarioultmod=usuario, usuarioreg=usuario,id_aula=id_aula, id_grupo=id_grupo)
            nueva_rel.save()
        relA = rel_aula_grupo.objects.filter(id_grupo=id_grupo)
        Aulas_F =Aula.objects.all()
        for x in relA:
            Aulas_F = Aulas_F.exclude(pk=x.id_aula)
        Aulas = Aula.objects.all()
        Context = {
            'GrupoF': GrupoF,
            'RelA': relA,
            'Aulas': Aulas,
            'Aulas_f': Aulas_F
        }
        data = {'rendered_table': render_to_string(
            'tablas_aulas.html', context=Context)}
        return JsonResponse(data)

@login_required(login_url='inicio')
def pagos(request):
    pagos = Pago.objects.filter(tipo_registro=1)
    alumnos = Alumno.objects.all()
    adeudos = Adeudos.objects.all()
    for x in pagos:
        x.fechareg = x.fechareg.strftime("%d-%m-%Y")
    Context = {
        'Pagos': pagos,
        'Alumnos': alumnos,
        'Adeudos': adeudos
    }
    if request.method == 'POST':
        if 'registrarPago' in request.POST:
            idAlumno = request.POST['Rid']
            tipoPago = request.POST['Rtipopago']
            metodoPago = request.POST.get('Rmetodopago', '')
            fechaPago = request.POST.get('Rfechapago', '')
            fechaProxima = request.POST.get('Rfechaproximo', '')
            promocion = request.POST.get('Rpromocion', '')
            referencia = request.POST.get('Rreferencia', '')
            cantidad = request.POST['Rcantidad']
            adeudo = request.POST.get('adeudocantidad', '')
            idadeudo = request.POST.get('Radeudo', '')
            usuario = request.user.username
            caja = Caja.objects.last()
            help = CajaHelp.objects.first()
            if metodoPago=='Efectivo':
                if caja.fechareg != help.fechaultcaja or caja.activa==False:
                    return HttpResponseRedirect("/caja/")
            if fechaPago == '':
                pago_nuevo = Pago(id_registro=idAlumno, tipo_registro=1, tipo_pago=tipoPago, metodo_pago=metodoPago, fechaPago=None,
                                promocion=promocion, referencia=referencia, cantidad=cantidad, usuarioreg=usuario, usuarioultmod=usuario)
                pago_nuevo.save() 

                # Registro de campos para tabla RegistroCaja, creación de historial de movimientos en caja
                registroNvoCaja = RegistroCaja(tipo='Ingreso', monto=cantidad, motivo = 'Pago por alumno', usuarioreg=usuario, usuarioultmod=usuario, 
                fechaultmod =datetime.datetime.now(), fechareg=datetime.datetime.now())
                # Registro de ultimo movimiento en caja generado
                registroNvoCaja.save()

                # Registro de campos para tabla Caja, nuevo objeto
                ultimoRegistroCaja = Caja.objects.latest('id') #Se obtiene ultimo dato de caja para hacer el acumulado
                nvoRegistroCaja = Caja(cantidad = float(ultimoRegistroCaja.cantidad)+float(cantidad),activa=True,usuarioreg=usuario,usuarioultmod=usuario,
                fechareg = datetime.datetime.now(), fechaultmod = datetime.datetime.now())
                # Se guarda el objeto generado de el nvo registro de caja
                nvoRegistroCaja.save()

            else:
                pago_nuevo = Pago(id_registro=idAlumno, tipo_registro=1, tipo_pago=tipoPago, metodo_pago=metodoPago, fechaPago=fechaPago,
                                promocion=promocion, referencia=referencia, cantidad=cantidad, usuarioreg=usuario, usuarioultmod=usuario)
                pago_nuevo.save()

            if idadeudo != "" and adeudo == "0":
                # se liquida adeudo
                pk = idadeudo.split("-")[1]
                Adeudos.objects.filter(pk=pk, tipo_adeudo=1).update(
                    activo=False, cantidad_adeudo=0,fechaProxima=None, fecha_liquidacion=datetime.datetime.now(),fechaultmod=datetime.datetime.now(),usuarioultmod=usuario)
                return HttpResponseRedirect("/pagos/")
            elif idadeudo != "" and adeudo != 0:
                # se abona a adeudo
                pk = idadeudo.split("-")[1]
                adeudoF = Adeudos.objects.get(pk=pk, tipo_adeudo=1)
                resta = adeudoF.cantidad_adeudo-float(adeudo)
                Adeudos.objects.filter(pk=pk, tipo_adeudo=1).update(
                    cantidad_adeudo=resta,fechaProxima=fechaProxima,fechaultmod=datetime.datetime.now(),usuarioultmod=usuario)
                return HttpResponseRedirect("/pagos/")
            elif idadeudo == "" and int(adeudo) != 0:
                # se genera nuevo adeudo
                nuevo_adeudo = Adeudos(id_registro=idAlumno,id_pago=pago_nuevo.pk, tipo_adeudo=1, cantidad_adeudo=adeudo,fechaProxima=fechaProxima,
                                    activo=True, fecha_liquidacion=None, usuarioreg=usuario, usuarioultmod=usuario)
                nuevo_adeudo.save()
                return HttpResponseRedirect("/pagos/")
            else:
                return HttpResponseRedirect("/pagos/")
    return render(request, 'pagos.html', Context)



def modalPagos(request, id_alumno=None, id_pago=None):
    Pagos = Pago.objects.filter(tipo_registro=1)
    Alumnos = Alumno.objects.all()
    Promociones = Promocion.objects.all()
    if id_alumno is not None:
        # este if ayuda a la consulta dinamica de los grupos y adeudos
        rel = rel_alu_doc_grupo.objects.filter(id_alumno=id_alumno)
        grupos = Grupo.objects.all()
        cursos = Curso.objects.all()
        aulas = Aula.objects.all()
        adeudos = Adeudos.objects.filter(id_registro=id_alumno)
        Context = {
            'Grupos': grupos,
            'Rel': rel,
            'Cursos': cursos,
            'Aulas': aulas,
            'Adeudos': adeudos
        }
        data = {'rendered_table': render_to_string(
            'combos_pagos.html', context=Context)}
        return JsonResponse(data)
    elif id_pago is not None:
        pago = Pago.objects.get(pk=id_pago, tipo_registro=1)
        Alumnos = Alumno.objects.all()
        if pago.referencia == "":
            pago.referencia = "- pago realizado en efectivo-"
        if pago.fechaPago != None:
            pago.fechaPago = pago.fechaPago.strftime("%Y-%m-%d")
        pago.fechareg = pago.fechareg.strftime("%Y-%m-%d")
        Context = {
            'Pago': pago,
            'Alumnos': Alumnos
        }
        return render(request, 'modales.html', Context)
    else:
        Context = {
            'Alumnos': Alumnos,
            'Promociones': Promociones,
        }
        return render(request, 'modales.html', Context)

@login_required(login_url='inicio')
def pagos_d(request):
    docentes = Docente.objects.all()
    pagos = Pago.objects.filter(tipo_registro=2)
    for x in pagos:
        x.fechareg = x.fechareg.strftime("%d-%m-%Y")
    Context = {
        'Docentes': docentes,
        'Pagos': pagos,
    }
    if request.method == 'POST':
        if 'registrarPago' in request.POST:
            idDocente = request.POST['Rid']
            tipoPago = request.POST['Rtipopago']
            metodoPago = request.POST.get('Rmetodopago', '')
            fechaPago = request.POST.get('Rfechapago', '')
            referencia = request.POST.get('Rreferencia', '')
            cantidad = request.POST['Rcantidad']
            usuario = request.user.username
            caja = Caja.objects.last()
            help = CajaHelp.objects.first()
            if metodoPago=='Efectivo':
                if caja.fechareg != help.fechaultcaja or caja.activa==False:
                    return HttpResponseRedirect("/caja/")
            if fechaPago == '':
                pago_nuevo = Pago(id_registro=idDocente, tipo_registro=2, tipo_pago=tipoPago, metodo_pago=metodoPago, fechaPago=None,
                                promocion=0, referencia=referencia, cantidad=cantidad, usuarioreg=usuario, usuarioultmod=usuario)
                pago_nuevo.save()

                # Registro de campos para tabla RegistroCaja, creación de historial de movimientos en caja
                registroNvoCaja = RegistroCaja(tipo='Egreso', monto=cantidad, motivo = 'Pago a docente', usuarioreg=usuario, usuarioultmod=usuario,
                    fechaultmod =datetime.datetime.now(), fechareg=datetime.datetime.now())
                # Se guarda el objeto generado de el nvo movimiento en caja
                registroNvoCaja.save()

                # Registro de campos para tabla Caja, nuevo objeto
                ultimoRegistroCaja = Caja.objects.latest('id') #Se obtiene ultimo dato de caja para hacer el acumulado
                nvoRegistroCaja = Caja(cantidad = float(ultimoRegistroCaja.cantidad)-float(cantidad),activa=True,usuarioreg=usuario,usuarioultmod=usuario,
                fechareg = datetime.datetime.now(), fechaultmod = datetime.datetime.now())
                # Se guarda el objeto generado de el nvo registro de caja
                nvoRegistroCaja.save()
                return HttpResponseRedirect("/pagos_d/")
            else:
                pago_nuevo = Pago(id_registro=idDocente, tipo_registro=2, tipo_pago=tipoPago, metodo_pago=metodoPago, fechaPago=fechaPago,
                                promocion=0, referencia=referencia, cantidad=cantidad, usuarioreg=usuario, usuarioultmod=usuario)
                pago_nuevo.save()
                return HttpResponseRedirect("/pagos_d/")
    return render(request, 'pagos_docentes.html', Context)

def modalPagosD(request, id_pago=None):
    docentes = Docente.objects.all()
    pagoF = Pago.objects.get(pk=id_pago,tipo_registro=2)
    if pagoF.fechaPago != None:
        pagoF.fechaPago = pagoF.fechaPago.strftime("%Y-%m-%d")
    pagoF.fechareg = pagoF.fechareg.strftime("%Y-%m-%d")
    Context = {
        'PagoF':pagoF,
        'Docentes': docentes
    }
    return render(request, 'modales.html', Context)

@login_required(login_url='inicio')
def ventas(request):
    caja = Caja.objects.last()
    usuario = request.user.username
    help = CajaHelp.objects.first()
    if caja.fechareg!= help.fechaultcaja or caja.activa==False:
        return HttpResponseRedirect("/caja/")
    else:
        Productos = Producto.objects.all()
        Libros = Libro.objects.all()
        Alumnos = Alumno.objects.all()
        Context = {
            'Productos':Productos,
            'Libros':Libros,
            'Alumnos':Alumnos
        }
    if request.method == 'POST':
        listaProductos = Producto.objects.all()
        listaLibros = Libro.objects.all()
        # Registro de campos para tabla venta 
        id_cliente = request.POST['inputIdCliente']
        total = request.POST['totalVenta']
        cantPagada = request.POST['Rcantidad']
        
        # Se genera el objeto nuevaVenta con los datos obtenidos 
        nuevaVenta = Venta(id_cliente = id_cliente, total = total, cantPagada = cantPagada, 
        usuarioreg = usuario, usuarioultmod = usuario, fechareg = datetime.datetime.now(), fechaultmod = datetime.datetime.now())

        # Se guarda el objeto generado de la nuevaVenta
        nuevaVenta.save()
        
        # Registro de campos para tabla detalleVenta
        # TODO: id_venta colocar este campo que se autoincremente.
        # TODO: Agregar precio unitario al producto (Detalle_centa)
        monto = request.POST.getlist('precioP')
        id_producto = request.POST.getlist('idProducto')
        tipoProducto = request.POST.getlist('TipoProducto')
        try:
            field_name = 'id_venta'
            obj = Detalle_venta.objects.latest('id')
            field_object = Detalle_venta._meta.get_field(field_name)
            ultimoRegistroDetalleVenta = field_object.value_from_object(obj)
            #ultimoRegistroDetalleVenta = Detalle_venta.objects.latest('id_venta')
            #print('1',ultimoRegistroDetalleVenta)
        except:
            ultimoRegistroDetalleVenta = 0
        ultimoRegistroDetalleVenta += 1
        #print('2',ultimoRegistroDetalleVenta)
        for idx, c in enumerate(request.POST.getlist('cantidadP')):
            
            # Se genera el monto (cantidad * precio)
            m = float(monto[idx])*float(c)

            # Se genera un objeto por cada ciclo recorrido (productos)
        
            # print(nuevoDetalleV.id_venta, nuevoDetalleV.id_producto, nuevoDetalleV.cantidad, nuevoDetalleV.monto, nuevoDetalleV.usuarioreg)
            if tipoProducto[idx] == 'Producto':
                nuevoDetalleV = Detalle_venta(id_venta = ultimoRegistroDetalleVenta, id_producto = id_producto[idx], tipoProducto=tipoProducto[idx],cantidad = c, monto = m, usuarioreg = usuario, usuarioultmod = usuario, fechareg = datetime.datetime.now(), fechaultmod = datetime.datetime.now())
                nuevoDetalleV.save()
                # Se resta la cantidad de c al inventario de ese producto (consultar inventario(id_producto=id_producto[idx]))
                # Sacar el campo del inventario del producto con id_producto[idx]
                objInventario = listaProductos.filter(id = id_producto[idx])
                prueba = Producto.objects.filter(id = id_producto[idx]) #se obtiene el producto a modificar su inventario
                # print(prueba[0].nombre)
                # print('indice:',idx)
                prueba2 = prueba[0]
                prueba2.inventario = float(objInventario[0].inventario) - float(c)
                prueba2.save()
            else:
                nuevoDetalleV = Detalle_venta(id_venta = ultimoRegistroDetalleVenta, id_producto = id_producto[idx], tipoProducto=tipoProducto[idx],cantidad = c, monto = m, usuarioreg = usuario, usuarioultmod = usuario, fechareg = datetime.datetime.now(), fechaultmod = datetime.datetime.now())
                nuevoDetalleV.save()
                # Se resta la cantidad de c al inventario de ese producto (consultar inventario(id_producto=id_producto[idx]))
                # Sacar el campo del inventario del producto con id_producto[idx]
                objInventario = listaLibros.filter(id = id_producto[idx])
                prueba = Libro.objects.filter(id = id_producto[idx])
                # print(prueba[0].nombre)
                # print('indice:',idx)
                prueba2 = prueba[0]
                prueba2.restantes = float(objInventario[0].restantes) - float(c)
                prueba2.vendidos +=1
                prueba2.save()      
            nuevoDetalleV.save()   
            

        # Registro de campos para tabla Adeudos generados de la venta
        cantidad_adeudo = float(request.POST['Rmonto'])
        if cantidad_adeudo > 0:
            id_registro = request.POST['inputIdCliente']
            ultVenta = Venta.objects.latest('id')
            id_pago = ultVenta.id #se debe guardar el id de la venta generada 
            fechaProxima = request.POST['Rfechaproximo']
            fecha_liquidacion = request.POST['Rfechaproximo']

            # Se genera el objeto nuevaVenta con los datos obtenidos 
            nuevoAdeudo = Adeudos(id_registro = id_registro, id_pago = id_pago, tipo_adeudo = 2, 
            cantidad_adeudo = cantidad_adeudo, activo=True, fechaProxima=fechaProxima, fecha_liquidacion=fecha_liquidacion, 
            usuarioreg = usuario, usuarioultmod = usuario, fechareg = datetime.datetime.now(), fechaultmod = datetime.datetime.now())

            # Se guarda el objeto generado de la nuevaVenta
            nuevoAdeudo.save()

        # Registro de campos para tabla Caja, nuevo objeto
        ultimoRegistroCaja = Caja.objects.latest('id') #Se obtiene ultimo dato de caja para hacer el acumulado
        nvoRegistroCaja = Caja(cantidad = float(ultimoRegistroCaja.cantidad)+float(cantPagada),activa=True,usuarioreg=usuario,usuarioultmod=usuario,
        fechareg = datetime.datetime.now(), fechaultmod = datetime.datetime.now())

        # Se guarda el objeto generado de el nvo registro de caja
        nvoRegistroCaja.save()

        # Registro de campos para tabla RegistroCaja, nuevo objeto
        registroNvoCaja = RegistroCaja(tipo='Ingreso', monto=cantPagada, id_venta = ultimoRegistroDetalleVenta, motivo = 'Venta', usuarioreg=usuario, usuarioultmod=usuario,
                    fechaultmod =datetime.datetime.now(), fechareg=datetime.datetime.now())
        
        # Se guarda el objeto generado de el nvo registro de caja
        registroNvoCaja.save()
        #TODO:ACTUALIZAR INVENTARIO SEGUN CORRESPONDA EL PRODUCTO
        #RESTANTES ES IGUAL A INVENTARIO EN LOS LIBROS Y TOTAL VENDIDOS NOMAS ES UN ++ DE LOS QUE SE VENDIERON
    return render(request,'ventas.html',Context)

@login_required(login_url='inicio')
def libros(request):
    libros = Libro.objects.all()
    Context = {
        'Libros': libros
    }
    if request.method == 'POST':
        if 'registrar' in request.POST:
            nombre = request.POST['Rnombre']
            idioma = request.POST['Ridioma']
            nivel = request.POST['Rnivel']
            precio = request.POST['Rprecio']
            cantidad = request.POST['Rcantidad']
            anotaciones = request.POST['Ranotaciones']
            usuario = request.user.username
            nuevo_libro= Libro(nombre=nombre,anotaciones=anotaciones,usuarioreg=usuario,usuarioultmod=usuario,
            cantidad=cantidad,nivel=nivel,idioma=idioma,precio=precio,fecha_inv=datetime.datetime.now(),vendidos=0,restantes=cantidad,
            agregados=0,total_en_venta=(float(precio)* int(cantidad)))
            nuevo_libro.save()
            return HttpResponseRedirect("/libros/")
        elif 'modificar' in request.POST:
            idmod = request.POST['modificar']
            nombre = request.POST['Mnombre']
            idioma = request.POST['Midioma']
            nivel = request.POST['Mnivel']
            precio = request.POST['Mprecio']
            anotaciones = request.POST['Manotaciones']
            usuario = request.user.username
            librof= Libro.objects.get(pk=idmod)
            Libro.objects.filter(pk=idmod).update(nombre=nombre,anotaciones=anotaciones,idioma=idioma,nivel=nivel,
            precio=precio,total_en_venta=(float(precio)* int(librof.restantes)),fechaultmod=datetime.datetime.now(),
            usuarioultmod=usuario)
            return HttpResponseRedirect("/libros/")
        elif 'agregar' in request.POST:
            idmod = request.POST['agregar']
            agregados = request.POST['Acantidad']
            usuario = request.user.username
            librof= Libro.objects.get(pk=idmod)
            restantes_nuevo=int(librof.restantes)+int(agregados)
            Libro.objects.filter(pk=idmod).update(agregados=agregados,restantes=restantes_nuevo,
            total_en_venta=(restantes_nuevo*int(librof.precio)),fechaultmod=datetime.datetime.now(),usuarioultmod=usuario)
            return HttpResponseRedirect("/libros/")
    return render(request, 'libros.html', Context)

def modalLibros(request, id=None):
    Libro_f = Libro.objects.get(pk=id)
    Libro_f.fechareg = Libro_f.fechareg.strftime("%Y-%m-%d")
    Libro_f.fecha_inv = Libro_f.fecha_inv.strftime("%Y-%m-%d")
    print(Libro_f.fechareg, Libro_f.fecha_inv)
    return render(request, 'modales.html', {'Libro_f':Libro_f})

def modalDetalleVenta(request, id=None):
    Detalle_v = Detalle_venta.objects.filter(id_venta=id)
    Detalle_v2 = Detalle_venta.objects.filter(id_venta=id).first()
    Productos = Producto.objects.all()
    Libros = Libro.objects.all()
    return render(request, 'modales.html', {'Detalle_v': Detalle_v, 'Detalle_v2': Detalle_v2, 'Producto': Productos, 'Libro':Libros})


@login_required(login_url='inicio')
def inventario(request):
    productos = Producto.objects.all()
    Context = {
        'Productos': productos
    }
    if request.method == 'POST':
        if 'registrar' in request.POST:
            nombre = request.POST['Rnombre']
            precio = request.POST['Rprecio']
            cantidad = request.POST['Rcantidad']
            descripcion = request.POST['Rdescripcion']
            usuario = request.user.username
            nuevo_producto = Producto(nombre=nombre,precio=precio,inventario=cantidad,descripcion=descripcion,activo=True,
            usuarioreg=usuario,usuarioultmod=usuario)
            nuevo_producto.save()
            return HttpResponseRedirect("/inventario/")
        elif 'modificar' in request.POST:
            idmod = request.POST['modificar']
            nombre = request.POST['Mnombre']
            precio = request.POST['Mprecio']
            cantidad = request.POST['Mcantidad']
            descripcion = request.POST['Mdescripcion']
            usuario = request.user.username
            Producto.objects.filter(pk=idmod).update(nombre=nombre,precio=precio,inventario=cantidad,descripcion=descripcion,
            fechaultmod=datetime.datetime.now(),usuarioultmod=usuario)
            return HttpResponseRedirect("/inventario/")      
        elif 'eliminar' in request.POST:
            iddel = request.POST['eliminar']
            usuario = request.user.username
            Producto.objects.filter(pk=iddel).update(activo=False,fechaultmod=datetime.datetime.now(),usuarioultmod=usuario)
            return HttpResponseRedirect("/inventario/")      
    return render(request, 'inventario.html', Context)

def modalProducto(request, id=None):
    Producto_f = Producto.objects.get(pk=id)
    return render(request, 'modales.html', {'Producto_f':Producto_f})

@login_required(login_url='inicio')
def caja(request):
    HistorialCaja = RegistroCaja.objects.all()
    cajas = Caja.objects.all()
    if not cajas:
        if 'registrar' in request.POST:
            monto = request.POST['Rmonto']
            usuario = request.user.username
            Caja(cantidad=monto,activa=True,usuarioreg=usuario,usuarioultmod=usuario).save()
            return HttpResponseRedirect("/cajacierre/")
    else:
        help = CajaHelp.objects.first()
        caja = cajas.last()
        if caja.fechareg != help.fechaultcaja:
            if 'registrar' in request.POST:
                monto = request.POST['Rmonto']
                usuario = request.user.username
                Caja(cantidad=monto,activa=True,usuarioreg=usuario,usuarioultmod=usuario).save()
                return HttpResponseRedirect("/caja/")
        elif caja.activa:
            print("simon esta activa")
            if 'cerrar' in request.POST:        
                id = request.POST['cerrar']
                usuario = request.user.username
                Caja.objects.filter(pk=id).update(usuarioultmod=usuario,fechaultmod=datetime.datetime.now(),activa=False)
                return HttpResponseRedirect("/caja/")
            elif 'retirar' in request.POST:
                cantidadRetiro = request.POST['RetiroCantidad']
                motivoRetiro = request.POST['RetiroMotivo']
                usuario = request.user.username
                ultimoRegistroCaja = Caja.objects.latest('id') #Se obtiene ultimo dato de caja para hacer el acumulado
                # Se hacen los ajustes para actualizar cantidad en caja
                # Registro de campos para tabla Caja, nuevo objeto
                nvoRegistroCaja = Caja(cantidad = float(ultimoRegistroCaja.cantidad)-float(cantidadRetiro),activa=True,usuarioreg=usuario,usuarioultmod=usuario,
                fechareg = datetime.datetime.now())
                # Se guarda el objeto generado de el nvo registro de caja
                nvoRegistroCaja.save()
                # Nuevo registro de historial para los movimientos en caja
                # Registro de campos para tabla RegistroCaja, nuevo objeto
                registroNvoCaja = RegistroCaja(tipo='Egreso',monto=cantidadRetiro, motivo = 'Retiro a caja', usuarioreg=usuario, usuarioultmod=usuario)
                # Se guarda el objeto generado de el nvo registro de caja
                registroNvoCaja.save()
                return HttpResponseRedirect("/caja/")
            elif 'ingresar' in request.POST:
                cantidadIngreso = request.POST['RegistroCantidad']
                motivoIngreso = request.POST['RegistroMotivo']
                usuario = request.user.username
                ultimoRegistroCaja = Caja.objects.latest('id') #Se obtiene ultimo dato de caja para hacer el acumulado
                # Se hacen los ajustes para actualizar cantidad en caja
                # Registro de campos para tabla Caja, nuevo objeto
                nvoRegistroCaja = Caja(cantidad = float(ultimoRegistroCaja.cantidad)+float(cantidadIngreso),activa=True,usuarioreg=usuario,usuarioultmod=usuario,
                fechareg = datetime.datetime.now())
                # Se guarda el objeto generado de el nvo registro de caja
                nvoRegistroCaja.save()
                # Nuevo registro de historial para los movimientos en caja
                # Registro de campos para tabla RegistroCaja, nuevo objeto
                registroNvoCaja = RegistroCaja(tipo='Ingreso',monto=cantidadIngreso, motivo = 'Ingreso a caja', usuarioreg=usuario, usuarioultmod=usuario)
                # Se guarda el objeto generado de el nvo registro de caja
                registroNvoCaja.save()
                return HttpResponseRedirect("/caja/")
            return render(request, 'cajacierre.html',{'Caja':caja, 'historial':HistorialCaja})
        else:
            return render(request, 'cajacierre.html',{'Caja':caja, 'historial':HistorialCaja}) 
    return render(request, 'caja.html',{})  

@login_required(login_url='inicio')
def cajacierre(request):
    HistorialCaja = RegistroCaja.objects.all()
    caja = Caja.objects.all().last()
    if 'cerrar' in request.POST:
            id = request.POST['cerrar']
            print(id)
            return HttpResponseRedirect("/caja/")
    return render(request, 'cajacierre.html',{'Caja':caja, 'historial':HistorialCaja})

@login_required(login_url='inicio')
def historialVentas(request):
    Ventas = Venta.objects.all()
    Alumnos = Alumno.objects.all()
    print(Ventas)
    print(Alumnos)
    return render(request, 'historialVentas.html',{'venta':Ventas, 'alumnos':Alumnos})
