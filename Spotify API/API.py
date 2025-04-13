import json
from dotenv import load_dotenv
import os
import requests

class API:
    # Cargo las variables de entorno desde el .env
    load_dotenv()

    # Se obtienen las credenciales de API de Spotify desde las variables de entorno
    clientId = os.getenv("CLIENT_ID")
    clientSecret = os.getenv("CLIENT_SECRET")

    def getAccessToken(self, client_id:str, client_secret:str):
        try:
                res = requests.post("https://accounts.spotify.com/api/token", 
                                    headers={"Content-Type": "application/x-www-form-urlencoded"}, 
                                    data={"grant_type": "client_credentials",
                                        "client_id": client_id,
                                        "client_secret": client_secret 
                                        })
                return res.json()['access_token']
        except Exception as e:
            print(e)
        

    token = getAccessToken(clientId, clientSecret)

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
        
    playlistId = extractPlaylistId('https://open.spotify.com/playlist/3sWwKAETNrcp41VnrfKeT1?si=73ba8407da3843a1&nd=1&dlsi=09786e13497c493a')

    def getPlayList(self, access_token: str, playlist_id):
        i = 0
        allResponses = []

        while True:

            try:
                result = requests.get(f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks?offset={i}&limit=100",
                                headers={"Authorization": f"Bearer {access_token}"})

                jsonResult = result.json()
                allResponses.append(jsonResult)
                i += 100

                if jsonResult['next'] is None or not jsonResult.get('next'):
                    break
            except Exception as e:
                print(f"An error occurred: {e}")
                break

        return allResponses

    # Descargar la información de la playlist en formato JSON
    jsonPlaylist = getPlayList(token, playlistId)

    with open('playlist.json', 'w', encoding='utf-8') as jsonFile:
        json.dump(jsonPlaylist, jsonFile, ensure_ascii=False, indent=4)