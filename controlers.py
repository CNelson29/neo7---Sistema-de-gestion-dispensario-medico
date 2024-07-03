from urllib.parse import urlparse
from flask import Flask, make_response, render_template, request, redirect, session, url_for, flash ,send_file
from config import Config
from forms import LoginForm, SignupForm
from models import User, mysql, init_db, query_db, execute_db
from flask_login import LoginManager,current_user, login_user, logout_user
from models import User,get_user
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.pdfgen import canvas
#-------------------------------------------------------------------------------------------------------v--------------------------------------------------------------------
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

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ parte usuarios y logeo





@app.route("/signup/", methods=["GET", "POST"])
def show_signup_form():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = SignupForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data
        # Creamos el usuario y lo guardamos
        user = User(len(user) + 1, name, email, password)
        user.append(user)
        # Dejamos al usuario logueado
        login_user(user, remember=True)
        next_page = request.args.get('next', None)
        if not next_page or urlparse(next_page).netloc != '':
            next_page = url_for('home')
        return redirect(next_page)
    return render_template("registro.html", form=form)

# Ruta para mostrar el formulario de registro
@app.route('/REGISTRO')
def registro():
    return render_template('registro.html')

# Ruta para manejar el registro de cuentas
@app.route('/ACCESO-REGISTRO', methods=['POST'])
def acceso_registro():
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirm_password']
    if password == confirm_password:
        execute_db('INSERT INTO usuarios (email, password) VALUES (%s, %s)', (email, password))
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

@app.route('/login', methods=['GET', 'POST'])
def loginFrom():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = get_user(form.email.data)
        if user is not None and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or urlparse(next_page).netloc != '':
                next_page = url_for('index')
            return redirect(next_page)
        else:
            flash('Credenciales inválidas', 'danger')
    
    return render_template('login.html', form=form)

# Ruta para el índice o página principal después del login
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    return redirect(url_for('loginFrom'))
# cierre de seccion 
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('loginFrom'))

@login_manager.user_loader
def load_user(user_id):
    for user in user:
        if user.id == int(user_id):
            return user
    return None
#--------------------------------------------------------------------------------------------------------------------------------------------------PDF
# Ruta para generar PDF de doctores
@app.route('/generate_pdf/doctores', methods=['GET'])
def generate_pdf_doctores():
    doctores = query_db('SELECT * FROM medicos')

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Título del documento
    p.setFont("Helvetica-Bold", 16)
    p.drawString(200, height - 50, 'Reporte de Doctores')
    
    # Encabezados de la tabla
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, height - 80, "ID")
    p.drawString(100, height - 80, "Nombre")
    p.drawString(200, height - 80, "Cédula")
    p.drawString(300, height - 80, "Tanda labor")
    p.drawString(400, height - 80, "Especialidad")
    p.drawString(500, height - 80, "Estado")
    p.drawString(600, height - 80, "Email")

    # Dibujar una línea debajo de los encabezados
    p.line(50, height - 90, 700, height - 90)

    y_offset = height - 110
    p.setFont("Helvetica", 10)

    for doctor in doctores:
        p.drawString(50, y_offset, str(doctor[0]))
        p.drawString(100, y_offset, str(doctor[1]))
        p.drawString(200, y_offset, str(doctor[2]))
        p.drawString(300, y_offset, str(doctor[3]))
        p.drawString(400, y_offset, str(doctor[4]))
        p.drawString(500, y_offset, str(doctor[5]))
        p.drawString(600, y_offset, str(doctor[6]))
        
        # Dibujar líneas divisorias
        p.line(50, y_offset + 10, 50, y_offset - 10)
        p.line(100, y_offset + 10, 100, y_offset - 10)
        p.line(200, y_offset + 10, 200, y_offset - 10)
        p.line(300, y_offset + 10, 300, y_offset - 10)
        p.line(400, y_offset + 10, 400, y_offset - 10)
        p.line(500, y_offset + 10, 500, y_offset - 10)
        p.line(600, y_offset + 10, 600, y_offset - 10)
        p.line(700, y_offset + 10, 700, y_offset - 10)

        y_offset -= 20

        if y_offset < 50:  # Agregar nueva página si el espacio se acaba
            p.showPage()
            y_offset = height - 50
            # Dibujar nuevamente el encabezado en la nueva página
            p.setFont("Helvetica-Bold", 12)
            p.drawString(50, y_offset, "ID")
            p.drawString(100, y_offset, "Nombre")
            p.drawString(200, y_offset, "Cédula")
            p.drawString(300, y_offset, "Tanda labor")
            p.drawString(400, y_offset, "Especialidad")
            p.drawString(500, y_offset, "Estado")
            p.drawString(600, y_offset, "Email")
            
            p.line(50, y_offset - 10, 700, y_offset - 10)
            y_offset -= 30

    p.save()
    buffer.seek(0)

    return send_file(buffer, as_attachment=True, download_name='reporte_doctores.pdf', mimetype='application/pdf')

# Ruta para generar PDF de fármacos
@app.route('/generate_pdf/farmacos', methods=['GET'])
def generate_pdf_farmacos():
    pacientes = query_db('SELECT * FROM pacientes')

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Título del documento
    p.setFont("Helvetica-Bold", 16)
    p.drawString(200, height - 50, 'Reporte de Farmacos')
    
    # Encabezados de la tabla
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, height - 80, "ID")
    p.drawString(100, height - 80, "Nombre")
    p.drawString(200, height - 80, "Cédula")
    p.drawString(300, height - 80, "Carnet")
    p.drawString(400, height - 80, "Tipo")
    p.drawString(500, height - 80, "Email")

    # Dibujar una línea debajo de los encabezados
    p.line(50, height - 90, 550, height - 90)

    y_offset = height - 110
    p.setFont("Helvetica", 10)

    for paciente in pacientes:
        p.drawString(50, y_offset, str(paciente[0]))
        p.drawString(100, y_offset, str(paciente[1]))
        p.drawString(200, y_offset, str(paciente[2]))
        p.drawString(300, y_offset, str(paciente[3]))
        p.drawString(400, y_offset, str(paciente[4]))
        p.drawString(500, y_offset, str(paciente[5]))
        y_offset -= 20
        if y_offset < 50:  # Agregar nueva página si el espacio se acaba
            p.showPage()
            y_offset = height - 50
            # Dibujar nuevamente el encabezado en la nueva página
            p.setFont("Helvetica-Bold", 12)
            p.drawString(50, y_offset, "ID")
            p.drawString(100, y_offset, "Nombre")
            p.drawString(200, y_offset, "Cédula")
            p.drawString(300, y_offset, "Carnet")
            p.drawString(400, y_offset, "Tipo")
            p.drawString(500, y_offset, "Email")
            p.line(50, y_offset - 10, 550, y_offset - 10)
            y_offset -= 30

    p.save()
    buffer.seek(0)

    return send_file(buffer, as_attachment=True, download_name='pacientes.pdf', mimetype='application/pdf')

# Ruta para generar PDF de marcas
@app.route('/generate_pdf/marcas', methods=['GET'])
def generate_pdf_marcas():
    marcas = query_db('SELECT * FROM marcas')

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Título del documento
    p.setFont("Helvetica-Bold", 16)
    p.drawString(200, height - 50, 'Reporte de Marcas')
    
    # Encabezados de la tabla
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, height - 80, "ID")
    p.drawString(100, height - 80, "Nombre")

    # Dibujar una línea debajo de los encabezados
    p.line(50, height - 90, 550, height - 90)

    y_offset = height - 110
    p.setFont("Helvetica", 10)

    for marca in marcas:
        p.drawString(50, y_offset, str(marca[0]))
        p.drawString(100, y_offset, str(marca[1]))
        y_offset -= 20
        if y_offset < 50:  # Agregar nueva página si el espacio se acaba
            p.showPage()
            y_offset = height - 50
            # Dibujar nuevamente el encabezado en la nueva página
            p.setFont("Helvetica-Bold", 12)
            p.drawString(50, y_offset, "ID")
            p.drawString(100, y_offset, "Nombre")
            p.line(50, y_offset - 10, 550, y_offset - 10)
            y_offset -= 30

    p.save()
    buffer.seek(0)

    return send_file(buffer, as_attachment=True, download_name='marcas.pdf', mimetype='application/pdf')

@app.route('/generate_pdf/pacientes', methods=['GET'])
def generate_pdf_pacientes():
    pacientes = query_db('SELECT * FROM pacientes')

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Título del documento
    p.setFont("Helvetica-Bold", 16)
    p.drawString(200, height - 50, 'Reporte de Pacientes')
    
    # Encabezados de la tabla
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, height - 80, "ID")
    p.drawString(100, height - 80, "Nombre")
    p.drawString(200, height - 80, "Cédula")
    p.drawString(300, height - 80, "Carnet")
    p.drawString(400, height - 80, "Tipo")
    p.drawString(500, height - 80, "Email")

    # Dibujar una línea debajo de los encabezados
    p.line(50, height - 90, 550, height - 90)

    y_offset = height - 110
    p.setFont("Helvetica", 10)

    for paciente in pacientes:
        p.drawString(50, y_offset, str(paciente[0]))
        p.drawString(100, y_offset, str(paciente[1]))
        p.drawString(200, y_offset, str(paciente[2]))
        p.drawString(300, y_offset, str(paciente[3]))
        p.drawString(400, y_offset, str(paciente[4]))
        p.drawString(500, y_offset, str(paciente[5]))
        y_offset -= 20
        if y_offset < 50:  # Agregar nueva página si el espacio se acaba
            p.showPage()
            y_offset = height - 50
            # Dibujar nuevamente el encabezado en la nueva página
            p.setFont("Helvetica-Bold", 12)
            p.drawString(50, y_offset, "ID")
            p.drawString(100, y_offset, "Nombre")
            p.drawString(200, y_offset, "Cédula")
            p.drawString(300, y_offset, "Carnet")
            p.drawString(400, y_offset, "Tipo")
            p.drawString(500, y_offset, "Email")
            p.line(50, y_offset - 10, 550, y_offset - 10)
            y_offset -= 30

    p.save()
    buffer.seek(0)

    return send_file(buffer, as_attachment=True, download_name='pacientes.pdf', mimetype='application/pdf')



if __name__ == '__main__':
    app.run(debug=True)


