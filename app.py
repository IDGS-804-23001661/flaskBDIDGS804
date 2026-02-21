from sqlalchemy.ext.asyncio import create_async_engine
from flask import Flask, render_template, request, redirect, url_for
from flask import flash
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
from flask import g 
import forms

from models import db
from models import Alumnos

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf=CSRFProtect()

@app.errorhandler(404)
def page_not_found(e):
	return render_template("404.html"),404

@app.route("/", methods=["GET", "POST"])
@app.route("/index")
def index():
    create_form = forms.UserForm(request.form)
    alumnos_list = Alumnos.query.all()
    return render_template("index.html", form=create_form, alumnos=alumnos_list)

@app.route("/Alumno", methods=['GET', 'POST'])
def alumnos():
	create_form=forms.UserForm(request.form)
	if request.method == 'POST':
		alum=Alumnos(nombre=create_form.nombre.data,
		apaterno=create_form.apaterno.data,
		email=create_form.email.data)
		db.session.add(alum)
		db.session.commit()
		return redirect(url_for('index'))
	return render_template("alumnos.html", form=create_form)

@app.route("/detalles", methods=['GET', 'POST'])
def detalles():
    id = request.args.get('id')
    alumno1 = Alumnos.query.get(id)
    if alumno1:
        nombre = alumno1.nombre
        apaterno = alumno1.apaterno
        email = alumno1.email
        return render_template("detalles.html", id=id, nombre=nombre, apaterno=apaterno, email=email)
    return redirect(url_for('index'))

@app.route("/modificar", methods=["GET", "POST"])
def modificar():
    id = request.args.get('id')
    alum = Alumnos.query.get(id)
    create_form = forms.UserForm(request.form, obj=alum)
    if request.method == 'POST' and create_form.validate():
        alum.nombre = create_form.nombre.data
        alum.apaterno = create_form.apaterno.data
        alum.email = create_form.email.data
        db.session.commit()
        return redirect(url_for('index'))
    return render_template("modificar.html", form=create_form)

@app.route("/eliminar", methods=["GET", "POST"])
def eliminar():
    id = request.args.get('id')
    alum = Alumnos.query.get(id)
    if request.method == 'POST':
        db.session.delete(alum)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template("eliminar.html", alum=alum)

if __name__ == '__main__':
	csrf.init_app(app)
	db.init_app(app)

	with app.app_context():
		db.create_all()
	
	app.run(debug=True)