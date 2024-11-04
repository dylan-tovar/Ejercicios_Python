from flask import Flask, render_template, request, redirect, url_for
import cmath
from collections import deque
from array import array

app = Flask(__name__)

@app.route('/menu')
def menu():
    return render_template('menu.html')

@app.route('/')
def home():
    return redirect(url_for('menu'))

# Funciones para el manejo del inventario
def verificar_inventario(producto):
    with open("1_inventario.txt", "r") as f:
        for line in f:
            partes = line.strip().split()
            if len(partes) != 2:
                continue
            nombre_producto, cantidad = partes
            if nombre_producto == producto and int(cantidad) > 0:
                return True
    return False

def actualizar_inventario(producto):
    lines = []
    with open("1_inventario.txt", "r") as f:
        for line in f:
            partes = line.strip().split()
            if len(partes) != 2:
                lines.append(line.strip())
                continue
            nombre_producto, cantidad = partes
            if nombre_producto == producto:
                cantidad = int(cantidad) - 1
            lines.append(f"{nombre_producto} {cantidad}")

    with open("1_inventario.txt", "w") as f:
        for line in lines:
            f.write(line + "\n")

def agregar_articulo(nombre_producto, cantidad):
    existe = False
    lines = []
    with open("1_inventario.txt", "r") as f:
        for line in f:
            partes = line.strip().split()
            if len(partes) == 2:
                nombre_existente, cantidad_existente = partes
                if nombre_existente == nombre_producto:
                    existe = True
                    cantidad_existente = int(cantidad_existente) + int(cantidad)
                    lines.append(f"{nombre_existente} {cantidad_existente}")
                else:
                    lines.append(line.strip())
    
    if not existe:
        lines.append(f"{nombre_producto} {cantidad}")

    with open("1_inventario.txt", "w") as f:
        for line in lines:
            f.write(line + "\n")

@app.route('/programa1_2', methods=['GET', 'POST'])
def programa1_2():
    mensaje = ""
    if request.method == 'POST':
        if 'agregar' in request.form:
            nombre_producto = request.form['nombre_producto']
            cantidad = request.form['cantidad']
            agregar_articulo(nombre_producto, cantidad)
            mensaje = f"El producto '{nombre_producto}' ha sido añadido con éxito."
            return render_template('programa1_2.html', accion='agregar', mensaje=mensaje)

        elif 'comprar' in request.form:
            producto = request.form['producto']
            if verificar_inventario(producto):
                actualizar_inventario(producto)
                mensaje = f"Has comprado el producto '{producto}' con éxito."
            else:
                mensaje = f"El producto '{producto}' no está disponible."
            return render_template('programa1_2.html', accion='comprar', mensaje=mensaje)

    return render_template('programa1_2.html', accion=request.args.get('accion'), mensaje=mensaje)

@app.route('/programa1', methods=['GET', 'POST'])
def programa1():
    return render_template('programa1.html')

@app.route('/programa2', methods=['GET', 'POST'])
def programa2():
    resultados = None
    if request.method == 'POST':
        # Obtener los valores de a, b, c del formulario
        a = float(request.form['a'])
        b = float(request.form['b'])
        c = float(request.form['c'])

        # Calcular discriminante D
        D = (b**2) - 4*(a*c)

        # Comprobando si el discriminante es mayor o igual que 0
        if D >= 0:
            # Calcular las raíces reales
            r1 = (-b - D**0.5) / (2 * a)
            r2 = (-b + D**0.5) / (2 * a)
            resultados = f"Las raíces reales son: {r1} y {r2}"
        else:
            # Calcular las raíces complejas
            r1 = (-b - cmath.sqrt(D)) / (2 * a)
            r2 = (-b + cmath.sqrt(D)) / (2 * a)
            resultados = f"Las raíces complejas son: {r1} y {r2}"

    return render_template('programa2.html', resultados=resultados)

@app.route('/programa3', methods=['GET', 'POST'])
def programa3():
    return render_template('programa3.html')

@app.route('/cocinar', methods=['POST'])
def cocinar():
    metodo = request.form.get('metodo')
    return render_template('programa3_1.html', metodo=metodo)

@app.route('/resultado', methods=['POST'])
def resultado():
    metodo = request.form.get('metodo')
    sal = request.form.get('sal')
    
    return render_template('programa3_2.html', metodo=metodo, sal=sal)

@app.route('/programa4', methods=['GET', 'POST'])
def programa4():
    return render_template('programa4.html')

@app.route('/lampara', methods=['GET', 'POST'])
def lampara():
    mensaje = ""
    if request.method == 'POST':
        enchufada = request.form.get('enchufada')
        quemada = request.form.get('quemada')
        cable_roto = request.form.get('cable_roto')

        if enchufada == "no":
            mensaje = "Enchufa la lámpara."
        elif quemada == "si":
            mensaje = "Cambia el bombillo."
        elif cable_roto == "si":
            mensaje = "Desenchúfa la lámpara y reempláza el cable."
        else:
            mensaje = "Compra una nueva lámpara."

    return render_template('programa4.html', mensaje=mensaje)


@app.route('/programa5', methods=['GET', 'POST'])
def programa5():
    return render_template('programa5.html')

@app.route('/decidir', methods=['POST'])
def programa5_1():
    decision = request.form.get('decision')
    if decision == 'si':
        mensaje = "Materia Prima Almacenada."
        return render_template('programa5_1.html', mensaje=mensaje, decision='si')
    elif decision == 'no':
        mensaje = "Procediendo a devolver o cambiar la materia prima."
        return render_template('programa5_1.html', mensaje=mensaje, decision='no')
    return redirect(url_for('programa5.html'))

@app.route('/control_si', methods=['POST'])
def control_si():
    return render_template ( 'programa5_2_si.html')

@app.route('/control_no', methods=['POST'])
def control_no():
    return render_template ( 'programa5_2_no.html')

@app.route('/pagar', methods=['POST'])
def pagar():
    return render_template ( 'programa5_2.html')

@app.route('/almacen', methods=['POST'])
def almacen():
    return render_template ( 'programa5_3.html')

@app.route('/comprar_panes', methods=['GET', 'POST'])
def comprar_panes():
    if request.method == 'POST':
        cantidad_canilla = int(request.form.get('cantidad_canilla', 0))
        cantidad_campesino = int(request.form.get('cantidad_campesino', 0))
        cantidad_dulce = int(request.form.get('cantidad_dulce', 0))
        cantidad_guayaba = int(request.form.get('cantidad_guayaba', 0))
        cantidad_queso = int(request.form.get('cantidad_queso', 0))

        # Verificar si al menos una cantidad es mayor que 0
        if (cantidad_canilla + cantidad_campesino + cantidad_dulce + 
            cantidad_guayaba + cantidad_queso) > 0:
            # Procesar la compra
            return redirect(url_for('factura'))  # Redirigir a la página de factura
        else:
            error_message = "Por favor, elige al menos un tipo de pan."
            return render_template('programa5_3.html', error_message=error_message)

    return render_template('programa5_3.html')

@app.route('/factura', methods=['GET', 'POST'])
def factura():
    return render_template('programa5_4.html')


@app.route('/programa6', methods=['GET', 'POST'])
def programa6():
    return render_template('programa6.html')   

@app.route('/credito', methods=['GET', 'POST'])
def credito():
    return render_template('programa6_1.html') 

@app.route('/capital', methods=['GET', 'POST'])
def capital():
    return render_template('programa6_2.html') 

@app.route('/prestamo', methods=['GET', 'POST'])
def prestamo():
    return render_template('programa6_3.html')

@app.route('/hola', methods=['GET', 'POST'])
def hola():
    return render_template('programa6_4.html')



class Municipio:
    def __init__(self, nombre):
        self.nombre = nombre
        self.siguiente = None

class Estado:
    def __init__(self, nombre):
        self.nombre = nombre
        self.municipios = None

    def agregar_municipio(self, nombre_municipio):
        nuevo_municipio = Municipio(nombre_municipio)
        if self.municipios is None:
            self.municipios = nuevo_municipio
        else:
            actual = self.municipios
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo_municipio

    def obtener_municipios(self):
        municipios_list = []
        actual = self.municipios
        while actual:
            municipios_list.append(actual.nombre)
            actual = actual.siguiente
        return municipios_list
    
estados = []

# Zulia
zulia = Estado("Zulia")
zulia.agregar_municipio("Almirante Padilla")
zulia.agregar_municipio("Baralt")
zulia.agregar_municipio("Cabimas")
zulia.agregar_municipio("Catatumbo")
zulia.agregar_municipio("Colón")
zulia.agregar_municipio("Francisco Javier Pulgar")
zulia.agregar_municipio("Jesús Enrique Losada")
zulia.agregar_municipio("Jesús María Semprún")

miranda = Estado("Miranda")
miranda.agregar_municipio("Caucagua")
miranda.agregar_municipio("San José de Barlovento")
miranda.agregar_municipio("Baruta")
miranda.agregar_municipio("Higuerote")
miranda.agregar_municipio("Mamporal")
miranda.agregar_municipio("Carrizal")
miranda.agregar_municipio("Chacao")
miranda.agregar_municipio("Charallave")
miranda.agregar_municipio("El Hatillo")
miranda.agregar_municipio("Los Teques")
miranda.agregar_municipio("Santa Teresa del Tuy")
miranda.agregar_municipio("Ocumare del Tuy")
miranda.agregar_municipio("San Antonio de los Altos")
miranda.agregar_municipio("Río Chico")
miranda.agregar_municipio("Santa Lucía")
miranda.agregar_municipio("Cúpira")
miranda.agregar_municipio("Guarenas")
miranda.agregar_municipio("San Francisco de Yare")
miranda.agregar_municipio("Petare")
miranda.agregar_municipio("Cúa")
miranda.agregar_municipio("Guatire")

# Carabobo
carabobo = Estado("Carabobo")
carabobo.agregar_municipio("Bejuma")
carabobo.agregar_municipio("Güigüe")
carabobo.agregar_municipio("Mariara")
carabobo.agregar_municipio("Guacara")
carabobo.agregar_municipio("Morón")
carabobo.agregar_municipio("Tocuyito")
carabobo.agregar_municipio("Los Guayos")
carabobo.agregar_municipio("Miranda")
carabobo.agregar_municipio("Montalbán")
carabobo.agregar_municipio("Naguanagua")
carabobo.agregar_municipio("Puerto Cabello")
carabobo.agregar_municipio("San Diego")
carabobo.agregar_municipio("San Joaquín")
carabobo.agregar_municipio("Valencia")

# Anzoátegui
anzoategui = Estado("Anzoátegui")
anzoategui.agregar_municipio("Anaco")
anzoategui.agregar_municipio("Aragua de Barcelona")
anzoategui.agregar_municipio("Barcelona")
anzoategui.agregar_municipio("Clarines")
anzoategui.agregar_municipio("Onoto")
anzoategui.agregar_municipio("Valle de Guanape")
anzoategui.agregar_municipio("Lechería")
anzoategui.agregar_municipio("Cantaura")
anzoategui.agregar_municipio("San José de Guanipa")
anzoategui.agregar_municipio("Guanta")
anzoategui.agregar_municipio("Soledad")
anzoategui.agregar_municipio("San Mateo")
anzoategui.agregar_municipio("El Chaparro")
anzoategui.agregar_municipio("Pariaguán")
anzoategui.agregar_municipio("San Diego de Cabrutica")
anzoategui.agregar_municipio("Puerto Píritu")
anzoategui.agregar_municipio("Píritu")
anzoategui.agregar_municipio("Boca de Uchire")
anzoategui.agregar_municipio("Santa Ana")
anzoategui.agregar_municipio("El Tigre")
anzoategui.agregar_municipio("Puerto La Cruz")


# Distrito Capital
DistritoCapital = Estado("Distrito Capital")
DistritoCapital.agregar_municipio("Caracas")

# Amazonas
Amazonas = Estado("Amazonas")
Amazonas.agregar_municipio("La Esmeralda")
Amazonas.agregar_municipio("San Fernando de Atabapo")
Amazonas.agregar_municipio("Puerto Ayacucho")
Amazonas.agregar_municipio("Isla Ratón")
Amazonas.agregar_municipio("San Juan de Manappire")
Amazonas.agregar_municipio("Maroa")
Amazonas.agregar_municipio("San Carlos de Río Negro")

# Apure
apure = Estado("Apure")
apure.agregar_municipio("Achaguas")
apure.agregar_municipio("Biruaca")
apure.agregar_municipio("Bruzual")
apure.agregar_municipio("Guasdualito")
apure.agregar_municipio("San Juan de Payara")
apure.agregar_municipio("Elorza")
apure.agregar_municipio("San Fernando de Apure")

# Aragua
aragua = Estado("Aragua")
aragua.agregar_municipio("San Mateo")
aragua.agregar_municipio("Camatagua")
aragua.agregar_municipio("Santa Rita")
aragua.agregar_municipio("Maracay")
aragua.agregar_municipio("Santa Cruz")
aragua.agregar_municipio("La Victoria")
aragua.agregar_municipio("El Consejo")
aragua.agregar_municipio("Palo Negro")
aragua.agregar_municipio("El Limón")
aragua.agregar_municipio("Ocumare de la Costa de Oro")
aragua.agregar_municipio("San Casimiro")
aragua.agregar_municipio("San Sebastián de los Reyes")
aragua.agregar_municipio("Turmero")
aragua.agregar_municipio("Las Tejerías")
aragua.agregar_municipio("Cagua")
aragua.agregar_municipio("Colonia Tovar")
aragua.agregar_municipio("Barbacoas")
aragua.agregar_municipio("Villa de Cura")


# Bolívar
bolivar = Estado("Bolívar")
bolivar.agregar_municipio("Ciudad Guayana")
bolivar.agregar_municipio("Caicara del Orinoco")
bolivar.agregar_municipio("El Callao")
bolivar.agregar_municipio("Santa Elena de Uairén")
bolivar.agregar_municipio("Ciudad Bolívar")
bolivar.agregar_municipio("Upata")
bolivar.agregar_municipio("Ciudad Piar")
bolivar.agregar_municipio("Guasipati")
bolivar.agregar_municipio("Tumeremo")
bolivar.agregar_municipio("Maripa")
bolivar.agregar_municipio("El Palmar")

barinas = Estado("Barinas")
barinas.agregar_municipio("Sabaneta")
barinas.agregar_municipio("El Cantón")
barinas.agregar_municipio("Socopó")
barinas.agregar_municipio("Arismendi")
barinas.agregar_municipio("Barinas")
barinas.agregar_municipio("Barinitas")
barinas.agregar_municipio("Barrancas")
barinas.agregar_municipio("Santa Bárbara")
barinas.agregar_municipio("Obispos")
barinas.agregar_municipio("Ciudad Bolivia")
barinas.agregar_municipio("Libertad")
barinas.agregar_municipio("Ciudad de Nutrias")

# Cojedes
cojedes = Estado("Cojedes")
cojedes.agregar_municipio("Cojedes")
cojedes.agregar_municipio("Tinaquillo")
cojedes.agregar_municipio("El Baúl")
cojedes.agregar_municipio("Macapo")
cojedes.agregar_municipio("El Pao")
cojedes.agregar_municipio("Libertad")

# Delta Amacuro
delta_amacuro = Estado("Delta Amacuro")
delta_amacuro.agregar_municipio("Curiapo")
delta_amacuro.agregar_municipio("Sierra Imataca")
delta_amacuro.agregar_municipio("Pedernales")
delta_amacuro.agregar_municipio("Tucupita")

falcón = Estado("Falcón")
falcón.agregar_municipio("San Juan de los Cayos")
falcón.agregar_municipio("San Luis")
falcón.agregar_municipio("Capatárida")
falcón.agregar_municipio("Yaracal")
falcón.agregar_municipio("Punto Fijo")
falcón.agregar_municipio("La Vela de Coro")
falcón.agregar_municipio("Dabajuro")
falcón.agregar_municipio("Pedregal")
falcón.agregar_municipio("Pueblo Nuevo")
falcón.agregar_municipio("Churuguara")
falcón.agregar_municipio("Jacura")
falcón.agregar_municipio("Santa Cruz de Los Taques")
falcón.agregar_municipio("Mene de Mauroa")
falcón.agregar_municipio("Santa Ana de Coro")
falcón.agregar_municipio("Chichiriviche")
falcón.agregar_municipio("Palmasola")
falcón.agregar_municipio("Cabure")
falcón.agregar_municipio("Píritu")
falcón.agregar_municipio("Mirimire")
falcón.agregar_municipio("Tucacas")
falcón.agregar_municipio("La Cruz de Taratara")
falcón.agregar_municipio("Tocópero")
falcón.agregar_municipio("Santa Cruz de Bucaral")
falcón.agregar_municipio("Urumaco")
falcón.agregar_municipio("Puerto Cumarebo")

guarico = Estado("Guárico")
guarico.agregar_municipio("Camaguan")
guarico.agregar_municipio("Chaguaramas")
guarico.agregar_municipio("El Socorro")
guarico.agregar_municipio("Calabozo")
guarico.agregar_municipio("Tucupido")
guarico.agregar_municipio("Altagracia de Orituco")
guarico.agregar_municipio("San Juan de Los Morros")
guarico.agregar_municipio("El Sombrero")
guarico.agregar_municipio("Las Mercedes")
guarico.agregar_municipio("Valle de La Pascua")
guarico.agregar_municipio("Zaraza")
guarico.agregar_municipio("Ortíz")
guarico.agregar_municipio("Guayabal")
guarico.agregar_municipio("San José de Guaribe")
guarico.agregar_municipio("Santa María de Ipire")

lara = Estado("Lara")
lara.agregar_municipio("Sanare")
lara.agregar_municipio("Duaca")
lara.agregar_municipio("Barquisimeto")
lara.agregar_municipio("Quibor")
lara.agregar_municipio("El Tocuyo")
lara.agregar_municipio("Cabudare")
lara.agregar_municipio("Sarare")
lara.agregar_municipio("Carora")
lara.agregar_municipio("Siquisique")

merida = Estado("Mérida")
merida.agregar_municipio("El Vigía")
merida.agregar_municipio("La Azulita")
merida.agregar_municipio("Santa Cruz de Mora")
merida.agregar_municipio("Lagunillas")
merida.agregar_municipio("Tovar")
merida.agregar_municipio("Nueva Bolivia")
merida.agregar_municipio("Zea")

monagas = Estado("Monagas")
monagas.agregar_municipio("San Antonio de Capayacuar")
monagas.agregar_municipio("Aguasai")
monagas.agregar_municipio("Bolívar")
monagas.agregar_municipio("Caripe")
monagas.agregar_municipio("Caicara")
monagas.agregar_municipio("Punta de Mata")
monagas.agregar_municipio("Temblador")
monagas.agregar_municipio("Maturín")
monagas.agregar_municipio("Aragua")
monagas.agregar_municipio("Quiriquire")
monagas.agregar_municipio("Santa Bárbara")
monagas.agregar_municipio("Barrancas del Orinco")
monagas.agregar_municipio("Uracoa")

nueva_esparta = Estado("Nueva Esparta")
nueva_esparta.agregar_municipio("La Plaza de Paraguachí")
nueva_esparta.agregar_municipio("La Asunción")
nueva_esparta.agregar_municipio("San Juan Bautista")
nueva_esparta.agregar_municipio("El Valle del Espíritu Santo")
nueva_esparta.agregar_municipio("Santa Ana")
nueva_esparta.agregar_municipio("Pampatar")
nueva_esparta.agregar_municipio("Juan Griego")
nueva_esparta.agregar_municipio("Porlamar")
nueva_esparta.agregar_municipio("Boca de Río")
nueva_esparta.agregar_municipio("Punta de Piedras")
nueva_esparta.agregar_municipio("San Pedro de Coche")

portuguesa = Estado("Portuguesa")
portuguesa.agregar_municipio("Agua Blanca")
portuguesa.agregar_municipio("Araure")
portuguesa.agregar_municipio("Píritu")
portuguesa.agregar_municipio("Guanare")
portuguesa.agregar_municipio("Guanarito")
portuguesa.agregar_municipio("Chabasquén de Unda")
portuguesa.agregar_municipio("Ospino")
portuguesa.agregar_municipio("Acarigua")
portuguesa.agregar_municipio("Papelón")
portuguesa.agregar_municipio("Boconoíto")
portuguesa.agregar_municipio("San Rafael de Onoto")
portuguesa.agregar_municipio("El Playón")
portuguesa.agregar_municipio("Biscucuy")
portuguesa.agregar_municipio("Villa Bruzual") 

sucre = Estado("Sucre")
sucre.agregar_municipio("Casanay")
sucre.agregar_municipio("San José de Aerocuar")
sucre.agregar_municipio("Río Caribe")
sucre.agregar_municipio("El Pilar")
sucre.agregar_municipio("Carúpano")
sucre.agregar_municipio("Yaguaraparo")
sucre.agregar_municipio("Araya")
sucre.agregar_municipio("Tunapuy")
sucre.agregar_municipio("Irapa")
sucre.agregar_municipio("San Antonio del Golfo")
sucre.agregar_municipio("Cumanacoa")
sucre.agregar_municipio("Cariaco")
sucre.agregar_municipio("Cumaná")
sucre.agregar_municipio("Güiria")

tachira = Estado("Táchira")
tachira.agregar_municipio("Andrés Bello")
tachira.agregar_municipio("Antonio Rómulo Costa")
tachira.agregar_municipio("Ayacucho")
tachira.agregar_municipio("Bolívar")
tachira.agregar_municipio("Cárdenas")
tachira.agregar_municipio("Córdoba")
tachira.agregar_municipio("Fernández Feo")
tachira.agregar_municipio("Francisco de Miranda")
tachira.agregar_municipio("García de Hevia")
tachira.agregar_municipio("Guásimos")
tachira.agregar_municipio("Independencia")
tachira.agregar_municipio("Jáuregui")
tachira.agregar_municipio("José María Vargas")
tachira.agregar_municipio("Junín")
tachira.agregar_municipio("San Judas Tadeo")
tachira.agregar_municipio("Libertad")
tachira.agregar_municipio("Libertador")
tachira.agregar_municipio("Lobatera")
tachira.agregar_municipio("Michelena")
tachira.agregar_municipio("Panamericano")
tachira.agregar_municipio("Pedro María Ureña")
tachira.agregar_municipio("Rafael Urdaneta")
tachira.agregar_municipio("Samuel Dario Maldonado")
tachira.agregar_municipio("San Cristóbal")
tachira.agregar_municipio("Seboruco")
tachira.agregar_municipio("Simón Rodríguez")
tachira.agregar_municipio("Sucre")
tachira.agregar_municipio("Torbes")
tachira.agregar_municipio("Uribante")

trujillo = Estado("Trujillo")
trujillo.agregar_municipio("Andrés Bello")
trujillo.agregar_municipio("Boconó")
trujillo.agregar_municipio("Bolívar")
trujillo.agregar_municipio("Candelaria")
trujillo.agregar_municipio("Carache")
trujillo.agregar_municipio("Escuque")
trujillo.agregar_municipio("José Felipe Márquez Cañizalez")
trujillo.agregar_municipio("Juan Vicente Campos Elías")
trujillo.agregar_municipio("La Ceiba")
trujillo.agregar_municipio("Miranda")
trujillo.agregar_municipio("Pampán")
trujillo.agregar_municipio("Trujillo")
trujillo.agregar_municipio("Andrés Linares")
trujillo.agregar_municipio("Pampanito")

la_guaira = Estado("La Guaira")
la_guaira.agregar_municipio("Vargas") 

yaracuy = Estado("Yaracuy")
yaracuy.agregar_municipio("Arístides Bastidas")
yaracuy.agregar_municipio("Bolívar")
yaracuy.agregar_municipio("Bruzual")
yaracuy.agregar_municipio("Cocorote")
yaracuy.agregar_municipio("Independencia")



estados.extend([ DistritoCapital, Amazonas, anzoategui, apure, aragua, barinas, bolivar, carabobo, cojedes, delta_amacuro, falcón, guarico, lara, merida, miranda, monagas, nueva_esparta, portuguesa, sucre, tachira, trujillo, la_guaira, yaracuy, zulia ])



@app.route('/arreglo2', methods=['GET', 'POST'])
def arreglo2():
    municipios = []
    selected_estado = None

    if request.method == 'POST':
        selected_estado = request.form.get('estado')
        if selected_estado:
            # Buscar el estado seleccionado
            for estado in estados:
                if estado.nombre == selected_estado:
                    municipios = estado.obtener_municipios()
                    break

    return render_template('arreglo2.html', estados=estados, municipios=municipios, selected_estado=selected_estado)





arreglo1_lista = []
# Rutas para el manejo de la lista en /arreglo1
@app.route('/arreglo1', methods=['GET', 'POST'])
def arreglo1():
    return render_template('arreglo1.html', lista=arreglo1_lista)

@app.route('/arreglo1/add', methods=['POST'])
def add_element():
    elemento = request.form.get('elemento')
    if elemento:
        arreglo1_lista.append(elemento)
    return redirect(url_for('arreglo1'))

@app.route('/arreglo1/pop_stack')
def pop_stack():
    if arreglo1_lista:
        arreglo1_lista.pop()
    return redirect(url_for('arreglo1'))

@app.route('/arreglo1/pop_queue')
def pop_queue():
    if arreglo1_lista:
        arreglo1_lista.pop(0)
    return redirect(url_for('arreglo1'))

@app.route('/arreglo1/view_tree')
def view_tree():
    tree_structure = []
    for i in range(len(arreglo1_lista)):
        left = 2 * i + 1
        right = 2 * i + 2
        node = {'value': arreglo1_lista[i], 'left': arreglo1_lista[left] if left < len(arreglo1_lista) else None,
                'right': arreglo1_lista[right] if right < len(arreglo1_lista) else None}
        tree_structure.append(node)
    return render_template('arreglo1.html', lista=arreglo1_lista, tree_structure=tree_structure)

# Función para la página de cola
@app.route('/estructuras/cola')
def cola():
    explicacion = "Una cola es una estructura FIFO (First In, First Out)."
    codigo = '''from collections import deque
cola = deque()
cola.append('A')
cola.append('B')
cola.append('C')
resultado = [cola.popleft(), list(cola)]  # ['A', ['B', 'C']]
'''
    cola = deque(['A', 'B', 'C'])
    resultado = [cola.popleft(), list(cola)]
    return render_template('estructura.html', nombre="Cola", explicacion=explicacion, codigo=codigo, resultado=resultado)

# Función para la página de pila
@app.route('/estructuras/pila')
def pila():
    explicacion = "Una pila es una estructura LIFO (Last In, First Out)."
    codigo = '''pila = []
pila.append('A')
pila.append('B')
pila.append('C')
resultado = [pila.pop(), pila]  # ['C', ['A', 'B']]
'''
    pila = ['A', 'B', 'C']
    resultado = [pila.pop(), pila]
    return render_template('estructura.html', nombre="Pila", explicacion=explicacion, codigo=codigo, resultado=resultado)

# Función para la página de árbol
@app.route('/estructuras/arbol')
def arbol():
    explicacion = "Un árbol binario tiene nodos con hijos izquierdo y derecho."
    codigo = '''class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izquierdo = None
        self.derecho = None

raiz = Nodo('A')
raiz.izquierdo = Nodo('B')
raiz.derecho = Nodo('C')
resultado = [raiz.valor, raiz.izquierdo.valor, raiz.derecho.valor]  # ['A', 'B', 'C']
'''
    class Nodo:
        def __init__(self, valor):
            self.valor = valor
            self.izquierdo = None
            self.derecho = None

    raiz = Nodo('A')
    raiz.izquierdo = Nodo('B')
    raiz.derecho = Nodo('C')
    resultado = [raiz.valor, raiz.izquierdo.valor, raiz.derecho.valor]
    return render_template('estructura.html', nombre="Árbol", explicacion=explicacion, codigo=codigo, resultado=resultado)

# Función para la página de grafo
@app.route('/estructuras/grafo')
def grafo():
    explicacion = "Un grafo tiene nodos conectados por aristas y se puede representar con un diccionario."
    codigo = '''grafo = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F'],
}
resultado = grafo['A']  # ['B', 'C']
'''
    grafo = {
        'A': ['B', 'C'],
        'B': ['A', 'D', 'E'],
        'C': ['A', 'F'],
    }
    resultado = grafo['A']
    return render_template('estructura.html', nombre="Grafo", explicacion=explicacion, codigo=codigo, resultado=resultado)

# Función para la página de arreglo
@app.route('/estructuras/arreglo')
def arreglo():
    explicacion = "Un arreglo es una estructura de tamaño fijo con acceso rápido por índice."
    codigo = '''from array import array
arreglo = array('i', [1, 2, 3, 4])
resultado = arreglo[2]  # 3
'''
    arreglo = array('i', [1, 2, 3, 4])
    resultado = arreglo[2]
    return render_template('estructura.html', nombre="Arreglo", explicacion=explicacion, codigo=codigo, resultado=resultado)

# Función para la página de hash
@app.route('/estructuras/hash')
def hash_table():
    explicacion = "Una tabla hash se implementa en Python usando un diccionario."
    codigo = '''tabla_hash = {'nombre': 'Juan', 'edad': 25}
resultado = tabla_hash  # {'nombre': 'Juan', 'edad': 25}
'''
    tabla_hash = {'nombre': 'Juan', 'edad': 25}
    resultado = tabla_hash
    return render_template('estructura.html', nombre="Hash", explicacion=explicacion, codigo=codigo, resultado=resultado)

# Función para la página de lista
@app.route('/estructuras/lista')
def lista_estructura():
    explicacion = "Una lista en Python es una estructura dinámica que permite agregar, eliminar y modificar elementos."
    codigo = '''mi_lista = [1, 2, 3]
mi_lista.append(4)
resultado = mi_lista  # [1, 2, 3, 4]
'''
    mi_lista = [1, 2, 3]
    mi_lista.append(4)
    resultado = mi_lista
    return render_template('estructura.html', nombre="Lista", explicacion=explicacion, codigo=codigo, resultado=resultado)

@app.route('/estructuras')
def estructuras():
    return render_template('estructuras_principal.html')



if __name__ == "__main__":
    app.run(debug=True)