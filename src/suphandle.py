from dotenv import load_dotenv
import os
load_dotenv()
from supabase import create_client
import requests
from datetime import datetime

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

supabase = create_client(url, key)

# Tareas:
# 1. Hacer una verificacion para ver corroborar si alguno de los datos YA existe en la tabla. Osea si ya existe una noticia con el mismo 'title' y 'location'.
# 2. Si existe, no la inserta. Si no existe, la inserta.
# 3. Endpoints para: 
#   - Obtener todos los eventos
#   - Obtener eventos por fecha 
#   - Obtener eventos por ubicación
#   - Obtener eventos por título
#   - Endpoint para eliminar eventos por ID
#   - Endpoint para actualizar eventos por ID
#   - Endpoint para agregar eventos desde el front (se deberan hacer algunas validaciones de datos antes de enviar)


# test_event = {
#     'title': 'Evento de prueba',
#     'location': 'Ubicación de prueba',
#     'latitude': 40.7128,
#     'longitude': -74.0060,
#     'time': '2023-10-01T12:00:00Z',
#     'publication_date': datetime.now().isoformat()  # Fecha actual como ejemplo
#     }

print(f"Conectando a Supabase: {url}")
print(f"Conectando a Supabase con la clave super secreta")
# insertacion_sup_events = supabase.table('events').insert(test_event).execute()



# Llamar a la API
news_api_url = os.environ.get("API_URL")
print(f"Estableciendo conexión a la API: {news_api_url}")
response = requests.get(news_api_url)
print(f"Conexión a la API establecida: {response.status_code}")

if response.status_code == 200:
    print("API llamada correctamente: ", response.status_code)
    data = response.json()
    print(f"Datos obtenidos de la API (data): {data}")

    # Extraer 'articles' o 'result' del JSON Porque la API a veces devuelve el array con las noticias adentro de una o de otra
    articles = data.get('articles') or data.get('result', [])
    print("Contenido de articles:", articles)

    # Verificar que 'articles' sea una lista
    if not isinstance(articles, list):
        print("Error: 'articles' no es una lista.")
        articles = []

    if len(articles) == 0:
        print("No hay artículos disponibles en la respuesta de la API.")
    else:
        events_to_insert = []
        for article in articles:
            # Verificar si "time" es "unknown" y asignar None si es el caso
            event_time = article.get('time')
            if event_time == "unknown":
                event_time = None

            event = {
                'title': article.get('title'),
                'location': article.get('location'),
                'latitude': article.get('coordinates', {}).get('latitude'),
                'longitude': article.get('coordinates', {}).get('longitude'),
                'time': event_time,
                'publication_date': datetime.now().isoformat()  # Fecha actual como ejemplo
            }
            events_to_insert.append(event)

        if events_to_insert:
            print(f"****Intentando insertar eventos****")
            for event in events_to_insert:
                print(f"Evento a insertar: {event}")
                # Insertar eventos en la tabla 'events' de Supabase
                insertacion_sup_table = supabase.table('events').insert(event).execute()
                if insertacion_sup_table:
                    print("Eventos insertados correctamente.")
                else:
                    print(f"Error al insertar eventos")
        else:
            print(f"No hay eventos para insertar.")
else:
    print(f"Error al obtener datos de la API: {response.status_code}")

sup_events_table = supabase.table('events').select('*').execute()
print(f"Aqui esta la tabla events: {sup_events_table}")