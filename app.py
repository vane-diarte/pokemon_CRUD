from flask import Flask, render_template, request, redirect, url_for, flash

import psycopg2
import psycopg2.extras
from datetime import datetime
import random 

app = Flask(__name__)

app.secret_key = "pokemon"
 

conn = psycopg2.connect(
    dbname= 'Pokemon', 
    user="postgres", 
    password= "123456",
    host="localhost")
 



@app.route('/')
def index():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT * FROM pokemones")
    lista_pokemon = cur.fetchall()
    cur.close()
    return render_template('index.html', lista_pokemon=lista_pokemon)


@app.route('/entrenadores')
def entrenadores():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT * FROM entrenadores")
    lista_entrenadores = cur.fetchall()
    cur.close()
    return render_template('entrenadores.html', lista_entrenadores=lista_entrenadores)


  

@app.route('/agregar_entrenador', methods=['POST'])
def agregar_entrenador():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        nombre = request.form['nombre']
        cur.execute("INSERT INTO entrenadores (nombre) VALUES (%s)", (nombre,))
        conn.commit()
        flash('Entrenador agregado', 'success')
        return redirect(url_for('entrenadores'))  


@app.route('/editar/<id>', methods = ['POST', 'GET'])
def editar_entrenador (id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('SELECT * FROM entrenadores WHERE id = %s', (id,))
    entrenador = cur.fetchone() #recupera todos los resultados de la consulta
    cur.close() #cierra el cursor
    return render_template('editar.html', entrenador = entrenador)


@app.route('/actualizar/<id>', methods = ['POST'])
def actualizar_entrenador(id):
    if request.method == 'POST':
        nombre = request.form['nombre']
         
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute (""" 
                    UPDATE entrenadores 
                    SET nombre = %s
                    WHERE id = %s """, (nombre, id))
        flash('Entrenador actualizado', 'success')
        conn.commit()
        return redirect(url_for('entrenadores'))
    
 
@app.route('/borrar/<id>', methods = ['POST','GET'])
def borrar_entrenador(id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
   
    cur.execute('DELETE FROM entrenadores WHERE id = {0}'.format(id))
    conn.commit()
    flash('Entrenador borrado', 'success')
    return redirect(url_for('entrenadores'))



@app.route('/asignar_pokemon', methods=['GET', 'POST'])
def asignar_pokemon_a_entrenador():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) #cursor para ejecutar comandos en la base de datos
    equipos_formados = [] # Lista para almacenar equipos formados

    if request.method == 'POST':
        # Obtención de IDs desde el formulario
        entrenador1_id = request.form['entrenador1']
        pokemon1_1 = request.form['pokemon1_1']
        pokemon1_2 = request.form['pokemon1_2']
        pokemon1_3 = request.form['pokemon1_3']

        entrenador2_id = request.form['entrenador2']
        pokemon2_1 = request.form['pokemon2_1']
        pokemon2_2 = request.form['pokemon2_2']
        pokemon2_3 = request.form['pokemon2_3']

        # Validaciones, si el id de ambos entrenadores son iguales o si el id de los pokemones guardados en el conjunto se repiten y son menores a 6... error!!
        if entrenador1_id == entrenador2_id or len({pokemon1_1, pokemon1_2, pokemon1_3, pokemon2_1, pokemon2_2, pokemon2_3}) != 6:
            flash('Debes seleccionar diferentes entrenadores y pokémones únicos para cada equipo.', 'danger')
        else:
            # Inserción en la tabla equipos para el primer equipo
            # RETURNING id solicita que despues de ingresar un nuevo registro la base de datos
            # devuelva el valor de la columna id del nuevo registro 
            cur.execute("""
                INSERT INTO equipos (pokemon1_id, pokemon2_id, pokemon3_id, entrenador_id, batalla_id)
                VALUES (%s, %s, %s, %s, NULL)
                RETURNING id 
            """, (pokemon1_1, pokemon1_2, pokemon1_3, entrenador1_id))
            equipo1_id = cur.fetchone()[0]

            # Inserción en la tabla equipos para el segundo equipo
            cur.execute("""
                INSERT INTO equipos (pokemon1_id, pokemon2_id, pokemon3_id, entrenador_id, batalla_id)
                VALUES (%s, %s, %s, %s, NULL)
                RETURNING id
            """, (pokemon2_1, pokemon2_2, pokemon2_3, entrenador2_id))
            equipo2_id = cur.fetchone()[0]

            conn.commit()

            # Registro de la batalla
            fecha_actual = datetime.now().date()
            ganador = random.choice([equipo1_id, equipo2_id])  # Selecciona al azar el ganador

            cur.execute("""
                INSERT INTO batallas (equipo1_id, equipo2_id, ganador, fecha)
                VALUES (%s, %s, %s, %s)
                RETURNING id
            """, (equipo1_id, equipo2_id, ganador, fecha_actual))
            batalla_id = cur.fetchone()[0]
            conn.commit()

            # Actualización de equipos con ID de batalla
            cur.execute("""
                UPDATE equipos SET batalla_id = %s WHERE id = %s
            """, (batalla_id, equipo1_id))
            cur.execute("""
                UPDATE equipos SET batalla_id = %s WHERE id = %s
            """, (batalla_id, equipo2_id))
            conn.commit()

            flash('Batalla creada y equipos formados', 'success')

            

    cur.execute("SELECT * FROM entrenadores")
    entrenadores = cur.fetchall() #variable para iterar al front
    cur.execute("SELECT * FROM pokemones")
    pokemones = cur.fetchall() #variable para iterar en el front
    cur.close()
    return render_template('asignar_pokemon.html', entrenadores=entrenadores, pokemones=pokemones)




@app.route('/batallas')
def mostrar_batallas():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) # cursor para ejecutar comandos en la base de datos

    # Obtener todas las batallas

    cur.execute("""
        SELECT batallas.id, batallas.fecha, equipo1.entrenador_id AS entrenador1_id, equipo2.entrenador_id AS entrenador2_id, batallas.ganador 
        FROM batallas
        JOIN equipos equipo1 ON batallas.equipo1_id = equipo1.id
        JOIN equipos equipo2 ON batallas.equipo2_id = equipo2.id
    """)
    batallas = cur.fetchall()

       
    equipos = []
    for batalla in batallas:

        # Obtener nombres de los entrenadores
        cur.execute("SELECT nombre FROM entrenadores WHERE id = %s", (batalla['entrenador1_id'],))
        entrenador1_nombre = cur.fetchone()['nombre']
        
        cur.execute("SELECT nombre FROM entrenadores WHERE id = %s", (batalla['entrenador2_id'],))
        entrenador2_nombre = cur.fetchone()['nombre']

        # Obtener nombre del ganador
        cur.execute("""
                SELECT equipos.entrenador_id, entrenadores.nombre
                FROM equipos
                JOIN entrenadores ON equipos.entrenador_id = entrenadores.id
                WHERE equipos.id = %s
            """, (batalla['ganador'],))
        ganador_info = cur.fetchone()
        ganador_nombre = ganador_info['nombre']
        
        equipos.append({
            'batalla_id': batalla['id'],
            'fecha': batalla['fecha'],
            'entrenador1': entrenador1_nombre,
            'entrenador2': entrenador2_nombre,
            'ganador': ganador_nombre
        })

    cur.close()
    return render_template('batallas.html', equipos=equipos)



if __name__ == '__main__':
    app.run(debug=True)




