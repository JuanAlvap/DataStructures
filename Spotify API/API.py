import json
from dotenv import load_dotenv
import os
import base64
from requests import post, get

# Cargo las variables de entorno desde el .env
load_dotenv()

# Se obtienen las credenciales de API de Spotify desde las variables de entorno
clientId = os.getenv("CLIENT_ID")
clientSecret = os.getenv("CLIENT_SECRET")

# Función para obtener el token de autenticacion (OAuth 2.0) de la API de Spotify
def getToken():
    authString = clientId + ':' + clientSecret
    # Se codifica el string de autenticacion a bytes y luego se codifica a base64 para obtener el string de autenticación en base64
    authBytes = authString.encode('utf-8')
    authBase64 = str(base64.b64encode(authBytes), "utf-8")
    
    url = 'https://accounts.spotify.com/api/token'

    # Se definen los headers y los datos que se enviaran en la peticion POST
    headers = {
        "Authorization": "Basic " + authBase64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "client_credentials"
    }

    # Se realiza la peticion POST y se obtiene el token de autenticación en formato JSON
    result = post(url, headers=headers, data=data)
    jsonResult = json.loads(result.content)
    # Se obtiene el token de autenticación y obtenemos esa parte del JSON
    token = jsonResult['access_token']
    return token

# Función para obtener el header de autenticación
def get_auth_header(token):
    return {
        "Authorization": "Bearer " + token
    }

# Función para extraer la parte del ID de la playlist
def extractPlaylistId(spotifyUrl):
    # Pregunta si la URL contiene '/playlist/' y si es asi, la divide en dos partes y se queda con la segunda parte
    if '/playlist/' in spotifyUrl:
        parts = spotifyUrl.split('/playlist/')[1]
        # Pregunta si la URL contiene '?' y si es asi, la divide en dos partes y se queda con la primera parte
        if '?' in parts:
            parts = parts.split('?')[0]
            return parts
        # Si no contiene '?' retorna la parte obtenida en el primer if
        else:
            return parts
    # Si no contiene '/playlist/' significa que no es una URL valida
    else:
        return None
    
playlistId = extractPlaylistId('https://open.spotify.com/playlist/1h1WOGO9v0YqCDwm2Lvncw')

# Función para obtener la información de una playlist
def getPlaylist(token, playlistId):
    # Se inicializa el controlador del offset en 0 y se crea una lista vacia para almacenar las respuestas en JSON de la API
    i = 0
    allResponses = []

    while True:

        # Se realiza la peticion GET a la API de Spotify para obtener la información de la playlist
        url = f"https://api.spotify.com/v1/playlists/{playlistId}/tracks?offset={i}&limit=100"
        headers = get_auth_header(token)
        result = get(url, headers=headers)

        # Si el status code de la respuesta no es 200, es decir, hubo un error, se imprime un mensaje de error y se rompe el ciclo
        if result.status_code != 200:
            print("Error al obtener la playlist")
            break

        # Se convierte la respuesta en JSON y se almacena en la lista de respuestas
        jsonResult = json.loads(result.content)
        allResponses.append(jsonResult)
        # Se aumenta el controlador del offset en 100 para obtener la siguiente parte de la playlist
        i += 100

        # Si el JSON de la respuesta no contiene la clave 'next' o si el valor de la clave 'next' es None,
        # Es decir que ya se obtuvo toda la información de la playlist y se rompe el ciclo
        if jsonResult['next'] == None or not jsonResult.get('next'):
            break
    
    # Se retorna la lista de respuestas en JSON
    return allResponses

# Descargar la información de la playlist en formato JSON
jsonPlaylist = getPlaylist(getToken(), playlistId)
with open('playlist.json', 'w', encoding='utf-8') as jsonFile:
    json.dump(jsonPlaylist, jsonFile, ensure_ascii=False, indent=4)