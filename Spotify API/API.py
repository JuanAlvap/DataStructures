import json
from dotenv import load_dotenv
import os
import requests

class API:

    def __init__(self):
        # Cargo las variables de entorno desde el .env
        load_dotenv()

        # Se obtienen las credenciales de API de Spotify desde las variables de entorno
        self.clientId = os.getenv("CLIENT_ID")
        self.clientSecret = os.getenv("CLIENT_SECRET")  
    
    # Función para obtener el token de acceso a la API de Spotify
    def getAccessToken(self, client_id:str, client_secret:str):
        # Se previene algun error en la petición
        try:
                # Se hace una petición POST a la API de Spotify para obtener el token de acceso
                res = requests.post("https://accounts.spotify.com/api/token", 
                                    headers={"Content-Type": "application/x-www-form-urlencoded"}, 
                                    data={"grant_type": "client_credentials",
                                        "client_id": client_id,
                                        "client_secret": client_secret 
                                        })
                # Se retorna el token de acceso en formato JSON
                return res.json()['access_token']
        except Exception as e:
            print(e)

    # Función para extraer la parte del ID de la playlist
    def extractPlaylistId(self, spotifyUrl):
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

    # Función para obtener la playlist completa
    def getPlayList(self, access_token: str, playlist_id):
        i = 0
        allResponses = []

        # Se hace un bucle infinito para obtener todas las canciones de la playlist hasta que no haya más canciones
        while True:
            # Se previene algun error en la petición
            try:
                # Se hace una petición GET a la API de Spotify para obtener la playlist
                result = requests.get(f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks?offset={i}&limit=100",
                                headers={"Authorization": f"Bearer {access_token}"})

                # Se almacena la respuesta en formato JSON, se añade a la lista de respuestas y se incrementa el offset 
                jsonResult = result.json()
                allResponses.append(jsonResult)
                i += 100
                # Se pregunta si el siguiente offset es None o no existe, si es asi se sale del bucle
                if jsonResult['next'] is None or not jsonResult.get('next'):
                    break

            except Exception as e:
                break
        
        # Se retorna la lista de respuestas
        return allResponses

    # Función para iniciar la API desde el Main y obtener la playlist completa
    def startAPI(self, playlist:str):
        token = self.getAccessToken(self.clientId, self.clientSecret)
        playlistId = self.extractPlaylistId(playlist)
        jsonPlaylist = self.getPlayList(token, playlistId)
        with open('playlist.json', 'w', encoding='utf-8') as jsonFile:
            json.dump(jsonPlaylist, jsonFile, ensure_ascii=False, indent=4)