from sqlalchemy.ext.asyncio import create_async_engine
from flask import Flask, render_template, request, redirect, url_for
from flask import flash
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
from flask import g 
from flask_migrate import Migrate
import forms

from models import db
from models import Alumnos

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
db.init_app(app)
migrate = Migrate(app, db)
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
		apellidos=create_form.apellidos.data,
		email=create_form.email.data,
		telefono=create_form.telefono.data)
		db.session.add(alum)
		db.session.commit()
		return redirect(url_for('index'))
	return render_template("alumnos.html", form=create_form)

@app.route("/modificar", methods=['GET', 'POST'])
def modificar():
    id = request.args.get('id')
    create_form = forms.UserForm(request.form)
    
    if request.method == 'GET':
        alum1 = Alumnos.query.get(id)
        if alum1:
            create_form.id.data = alum1.id
            create_form.nombre.data = alum1.nombre
            create_form.apellidos.data = alum1.apellidos
            create_form.email.data = alum1.email
            create_form.telefono.data = alum1.telefono

    if request.method == 'POST':
        alum1 = Alumnos.query.get(id)
        if alum1:
            alum1.nombre = create_form.nombre.data
            alum1.apellidos = create_form.apellidos.data
            alum1.email = create_form.email.data
            alum1.telefono = create_form.telefono.data
            db.session.commit()
            return redirect(url_for('index'))
            
    return render_template("modificar.html", form=create_form)

@app.route("/eliminar", methods=['GET', 'POST'])
def eliminar():
    id = request.args.get('id')
    create_form = forms.UserForm(request.form)
    
    if request.method == 'GET':
        alum1 = db.session.query(Alumnos).filter(Alumnos.id==id).first()
        create_form.id.data = request.args.get('id')
        create_form.nombre.data = alum1.nombre
        create_form.apellidos.data = alum1.apellidos
        create_form.email.data = alum1.email
        create_form.telefono.data = alum1.telefono

    if request.method == 'POST':
        alum1 = db.session.query(Alumnos).filter(Alumnos.id==id).first()
        db.session.delete(alum1)
        db.session.commit()
        return redirect(url_for('index'))
            
    return render_template("eliminar.html", form=create_form)

@app.route("/detalles", methods=['GET', 'POST'])
def detalles():
    id = request.args.get('id')
    alum = Alumnos.query.get(id)
    if alum:
        return render_template("detalles.html", id=id, nombre=alum.nombre, apellidos=alum.apellidos, email=alum.email, telefono=alum.telefono)
    return redirect(url_for('index'))

if __name__ == '__main__':
	csrf.init_app(app)

	with app.app_context():
		db.create_all()
	
	app.run(debug=True)