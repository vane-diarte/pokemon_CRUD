import requests
import psycopg2

conn = psycopg2.connect(
    dbname= 'Pokemon', 
    user="postgres", 
    password= "123456",
    host="localhost")

cursor = conn.cursor()


def cargar_pokemon(id):    
    api_url = f"https://pokeapi.co/api/v2/pokemon/{id}/"
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        name = data.get('name')
        number = data.get('id')
        type = data['types'][0]['type']['name']
        moves = data['moves'][0]['move']['name']
        

    
   
    

    cursor.execute("""
    INSERT INTO pokemones (nombre, tipo, habilidad, numero)
    VALUES (%s, %s, %s, %s)
    """,(name, type, moves, number))

    conn.commit()


for i in range (3,152):
    cargar_pokemon(i)

cursor.close()
conn.close()
