from flask import Flask, render_template, request, redirect, session, url_for, flash
from config import Config
from forms import LoginForm, SignupForm
from models import User, mysql, init_db, query_db, execute_db
from flask_login import LoginManager,current_user, get_user, login_user
from models import users
from werkzeug.urls import url_parse

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
app = Flask(__name__)
app.config.from_object(Config)
init_db(app)
app.config['SECRET_KEY'] = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'
login_manager = LoginManager(app)

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/HOME')
def home():
    return render_template('index.html')

@app.route('/agregar_farmaco')
def farmaco_agregado():
    return render_template('farmaco_registro.html')

@app.route('/tipos')
def tipos():
    tipos = query_db('SELECT * FROM tipos_farmacos')
    return render_template('tipos.html', tipos=tipos)

@app.route('/tipos/agregar', methods=['POST'])
def agregar_tipo():
    nombre = request.form['nombre']
    execute_db('INSERT INTO tipos_farmacos (nombre) VALUES (%s)', (nombre,))
    flash('Tipo de fármaco agregado exitosamente')
    return redirect(url_for('tipos'))

@app.route('/tipos/eliminar/<int:id>')
def eliminar_tipo(id):
    execute_db('DELETE FROM tipos_farmacos WHERE id = %s', (id,))
    flash('Tipo de fármaco eliminado exitosamente')
    return redirect(url_for('tipos'))

@app.route('/marcas')
def marcas():
    marcas = query_db('SELECT * FROM marcas')
    return render_template('marcas.html', marcas=marcas)

@app.route('/marcas/agregar', methods=['POST'])
def agregar_marca():
    nombre = request.form['nombre']
    execute_db('INSERT INTO marcas (nombre) VALUES (%s)', (nombre,))
    flash('Marca agregada exitosamente')
    return redirect(url_for('marcas'))

@app.route('/marcas/eliminar/<int:id>')
def eliminar_marca(id):
    execute_db('DELETE FROM marcas WHERE id = %s', (id,))
    flash('Marca eliminada exitosamente')
    return redirect(url_for('marcas'))

@app.route('/ubicaciones')
def ubicaciones():
    ubicaciones = query_db('SELECT * FROM ubicaciones')
    return render_template('ubicaciones.html', ubicaciones=ubicaciones)

@app.route('/ubicaciones/agregar', methods=['POST'])
def agregar_ubicacion():
    nombre = request.form['nombre']
    execute_db('INSERT INTO ubicaciones (nombre) VALUES (%s)', (nombre,))
    flash('Ubicación agregada exitosamente')
    return redirect(url_for('ubicaciones'))

@app.route('/ubicaciones/eliminar/<int:id>')
def eliminar_ubicacion(id):
    execute_db('DELETE FROM ubicaciones WHERE id = %s', (id,))
    flash('Ubicación eliminada exitosamente')
    return redirect(url_for('ubicaciones'))

@app.route('/farmacos')
def farmacos():
    farmacos = query_db('''
        SELECT f.id, f.nombre, t.nombre, m.nombre, u.nombre
        FROM farmacos f
        JOIN tipos_farmacos t ON f.tipo_id = t.id
        JOIN marcas m ON f.marca_id = m.id
        JOIN ubicaciones u ON f.ubicacion_id = u.id
    ''')
    tipos = query_db('SELECT * FROM tipos_farmacos')
    marcas = query_db('SELECT * FROM marcas')
    ubicaciones = query_db('SELECT * FROM ubicaciones')
    return render_template('farmacos.html', farmacos=farmacos, tipos=tipos, marcas=marcas, ubicaciones=ubicaciones)

@app.route('/farmacos/agregar', methods=['POST'])
def agregar_farmaco():
    nombre = request.form['nombre']
    tipo_id = request.form['tipo_id']
    marca_id = request.form['marca_id']
    ubicacion_id = request.form['ubicacion_id']
    execute_db('''
        INSERT INTO farmacos (nombre, tipo_id, marca_id, ubicacion_id)
        VALUES (%s, %s, %s, %s)
    ''', (nombre, tipo_id, marca_id, ubicacion_id))
    flash('Fármaco agregado exitosamente')
    return redirect(url_for('farmacos'))

@app.route('/farmacos/eliminar/<int:id>')
def eliminar_farmaco(id):
    execute_db('DELETE FROM farmacos WHERE id = %s', (id,))
    flash('Fármaco eliminado exitosamente')
    return redirect(url_for('farmacos'))

@app.route('/pacientes')
def pacientes():
    pacientes = query_db('SELECT * FROM pacientes')
    return render_template('paciente.html', pacientes=pacientes)

@app.route('/pacientes/agregar', methods=['POST'])
def agregar_paciente():
    nombre = request.form['nombre']
    cedula = request.form['cedula']
    carnet = request.form['carnet']
    tipoPaciente = request.form['tipoPaciente']
    email = request.form['email']
    calle = request.form['calle']
    localidad = request.form['localidad']
    ciudad = request.form['ciudad']
    password = request.form['password']
    execute_db('INSERT INTO pacientes (nombre, cedula, carnet, tipoPaciente,email,calle,localidad,ciudad,password) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)', (nombre,cedula, carnet, tipoPaciente,email, calle, localidad, ciudad, password))
    flash('Tipo de fármaco agregado exitosamente')
    return redirect(url_for('pacientes'))

@app.route('/pacientes/eliminar/<int:id>')
def eliminar_paciente(id):
    execute_db('DELETE FROM pacientes WHERE id = %s', (id,))
    flash('Tipo de fármaco eliminado exitosamente')
    return redirect(url_for('pacientes'))

@app.route('/doctores')
def doctores():
    doctores = query_db('SELECT * FROM medicos')
    return render_template('doctor.html', doctores=doctores)

@app.route('/doctores/agregar', methods = ['POST'])
def agregar_doctores():
        nombre = request.form['nombre']
        cedula = request.form['cedula']
        tanda = request.form['tanda']
        especialidad = request.form['especialidad']
        estado = request.form['estado']
        email = request.form['email']
        password = request.form['password']

        execute_db('INSERT INTO medicos(nombre,cedula,tanda_labor,especialidad,estado,email,password) VALUES (%s,%s,%s,%s,%s,%s,%s)',(nombre, cedula, tanda, especialidad, estado, email, password))
        flash('Datos guardados correctamente')
        return redirect(url_for('doctores'))

@app.route('/doctores/eliminar/<int:id>')
def eliminar_doctores(id):
    execute_db('DELETE FROM medicos WHERE id = %s', (id,))
    flash('Tipo de fármaco eliminado exitosamente')
    return redirect(url_for('doctores'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = get_user(form.email.data)
        if user is not None and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('index')
            return redirect(next_page)
    return render_template('login_form.html', form=form)

@app.route("/signup/", methods=["GET", "POST"])
def show_signup_form():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = SignupForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data
        # Creamos el usuario y lo guardamos
        user = User(len(users) + 1, name, email, password)
        users.append(user)
        # Dejamos al usuario logueado
        login_user(user, remember=True)
        next_page = request.args.get('next', None)
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template("signup_form.html", form=form)

# Ruta para mostrar el formulario de registro
@app.route('/REGISTRO')
def registro():
    return render_template('registro.html')

# Ruta para manejar el registro de cuentas
@app.route('/ACCESO-REGISTRO', methods=['POST'])
def acceso_registro():
    anynombre = request.form['nombre']
    anycorreo = request.form['correo']
    anypassword = request.form['password']
    any_password = request.form['password2']
    if anypassword == any_password:
        execute_db('INSERT INTO usuarios (nombre, email, password) VALUES (%s, %s, %s)', (anynombre, anycorreo, anypassword))
        return redirect(url_for('registro'))
    else:
        return render_template('registro.html', mensaje='No coinciden las contraseñas ingresadas')

# Ruta para manejar el login
@app.route('/ACCESO-LOGIN', methods=['GET', 'POST'])
def acceso_login():
    if request.method == 'POST' and 'txtcorreo' in request.form and 'txtpassword' in request.form:
        anycorreo = request.form['txtcorreo']
        anypassword = request.form['txtpassword']
        account = query_db('SELECT * FROM usuarios WHERE email = %s AND password = %s', (anycorreo, anypassword), one=True)
        if account:
            session['logueado'] = True
            session['id'] = account['id']
            session['nombre'] = account['nombre']
            return redirect(url_for('index'))
        else:
            return render_template('login.html', mensaje='Credenciales inválidas')
    return redirect(url_for('home'))

# Ruta para el índice o página principal después del login
@app.route('/')
def index():
    if 'logueado' in session:
        return redirect(url_for('home'))
    return redirect(url_for('login'))

@login_manager.user_loader
def load_user(user_id):
    for user in users:
        if user.id == int(user_id):
            return user
    return None

if __name__ == '__main__':
    app.run(debug=True)


