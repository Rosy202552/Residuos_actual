from flask import Flask, render_template, request, redirect, url_for
from models import db, Denuncia
import os

app = Flask(__name__, 
    template_folder='templates',  # Especificamos la carpeta de templates
    static_folder='static'        # Especificamos la carpeta de archivos estáticos
)

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///denuncias.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar la base de datos
db.init_app(app)

# Crear todas las tablas
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/menu')
def menu():
    return render_template('menu.html')

@app.route('/introduccion')
def introduccion():
    return render_template('introduccion.html')

@app.route('/tips')
def tips():
    return render_template('tips.html')

@app.route('/juego')
def juego():
    return render_template('juego.html')

# CRUD de denuncias
@app.route('/denuncias', methods=['GET', 'POST'])
def denuncias():
    if request.method == 'POST':
        nombre = request.form['nombre'] or "Anónimo"
        lugar = request.form['lugar']
        numero = (Denuncia.query.count() + 1)
        nueva = Denuncia(numero=numero, nombre=nombre, lugar=lugar)
        db.session.add(nueva)
        db.session.commit()
        return redirect(url_for('denuncias'))
    denuncias = Denuncia.query.all()
    return render_template('denuncias.html', denuncias=denuncias)

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    denuncia = Denuncia.query.get_or_404(id)
    if request.method == 'POST':
        denuncia.nombre = request.form['nombre'] or "Anónimo"
        denuncia.lugar = request.form['lugar']
        db.session.commit()
        return redirect(url_for('denuncias'))
    return render_template('editar_denuncia.html', denuncia=denuncia)

@app.route('/eliminar/<int:id>')
def eliminar(id):
    denuncia = Denuncia.query.get_or_404(id)
    db.session.delete(denuncia)
    db.session.commit()
    return redirect(url_for('denuncias'))

if __name__ == '__main__':
    app.run(debug=True)