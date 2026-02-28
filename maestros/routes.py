from . import maestros
from flask import render_template, request, redirect, url_for
import forms
from models import Maestros, db

@maestros.route('/perfil/<nombre>')
def perfil(nombre):
    return f"Perfil de {nombre}"

@maestros.route('/maestros', methods=['GET', 'POST'])
@maestros.route("/index")
def index():
    create_forms = forms.MaestroForm(request.form)
    maestros_list = Maestros.query.all()
    return render_template("maestros/listadoMaes.html", form=create_forms, maestros=maestros_list)

@maestros.route("/registrar", methods=['GET', 'POST'])
def registrar():
    create_form = forms.MaestroForm(request.form)
    if request.method == 'POST':
        maest = Maestros(matricula=create_form.matricula.data,
                         nombre=create_form.nombre.data,
                         apellidos=create_form.apellidos.data,
                         email=create_form.email.data,
                         especialidad=create_form.especialidad.data)
        db.session.add(maest)
        db.session.commit()
        return redirect(url_for('maestros.index'))
    return render_template("maestros/registrar.html", form=create_form)

@maestros.route("/modificar", methods=['GET', 'POST'])
def modificar():
    id = request.args.get('id')
    create_form = forms.MaestroForm(request.form)
    
    if request.method == 'GET':
        maest = Maestros.query.get(id)
        if maest:
            create_form.matricula.data = maest.matricula
            create_form.nombre.data = maest.nombre
            create_form.apellidos.data = maest.apellidos
            create_form.email.data = maest.email
            create_form.especialidad.data = maest.especialidad

    if request.method == 'POST':
        maest = Maestros.query.get(id)
        if maest:
            maest.nombre = create_form.nombre.data
            maest.apellidos = create_form.apellidos.data
            maest.email = create_form.email.data
            maest.especialidad = create_form.especialidad.data
            db.session.commit()
            return redirect(url_for('maestros.index'))
            
    return render_template("maestros/modificar.html", form=create_form)

@maestros.route("/eliminar", methods=['GET', 'POST'])
def eliminar():
    id = request.args.get('id')
    create_form = forms.MaestroForm(request.form)
    
    if request.method == 'GET':
        maest = Maestros.query.get(id)
        if maest:
            create_form.matricula.data = maest.matricula
            create_form.nombre.data = maest.nombre
            create_form.apellidos.data = maest.apellidos
            create_form.email.data = maest.email
            create_form.especialidad.data = maest.especialidad

    if request.method == 'POST':
        maest = Maestros.query.get(id)
        if maest:
            db.session.delete(maest)
            db.session.commit()
            return redirect(url_for('maestros.index'))
            
    return render_template("maestros/eliminar.html", form=create_form)

@maestros.route("/detalles", methods=['GET', 'POST'])
def detalles():
    id = request.args.get('id')
    maest = Maestros.query.get(id)
    if maest:
        return render_template("maestros/detalles.html", maest=maest)
    return redirect(url_for('maestros.index'))
