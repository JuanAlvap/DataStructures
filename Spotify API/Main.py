import AVL
import json
import ArtistClass
import API

songsTree = AVL.AVLTree()
artistsTree = AVL.AVLTree()
api = API.API()

playlist = 'https://open.spotify.com/playlist/3sWwKAETNrcp41VnrfKeT1?si=mpdPwjwwSEOCCkVXFqvPuQ'
# Se pregunta si se desea usar una playlist nueva o la predeterminada
condicion = input("¿Desea usar una playlist nueva? (s/n): ")
if (condicion == 's' or condicion == 'S'):
    playlist = input("Inserte la playlist: ")
# Se inicia la API de Spotify
api.startAPI(playlist)

with open('playlist.json', 'r', encoding='utf-8') as jsonFile:
    # Se carga el archivo JSON que contiene la información de la playlist
    jsonPlaylist = json.load(jsonFile)

    # Se recorre la lista de respuestas en JSON y se obtiene el id de la playlist
artistas_unicos = {} #lista de artistas totales del árbol como objetos
# Se valida si la playlist es valida para el análisis de datos
if int(jsonPlaylist[0]['error']['status']) == 404:
    print("Playlist no encontrada")
    print("Digite un playlist correcta")
else:
    # Si es valida se recorre la lista de respuestas en JSON
    for i in range(len(jsonPlaylist)):
        # Se recorre la lista de items
        for j in range(len(jsonPlaylist[i]['items'])):
            artistList = []
            # Se valida si hay tracks para acceder y no se encuentra vacio
            if jsonPlaylist[i]['items'][j]['track'] == None:
                continue
            # Se recorre la lista de artistas para obtener información relevante para nuestro análisis
            for k in range(len(jsonPlaylist[i]['items'][j]['track']['artists'])):
                artist = jsonPlaylist[i]['items'][j]['track']['artists'][k]['name']
                artistID = jsonPlaylist[i]['items'][j]['track']['artists'][k]['id']
                if artist not in artistas_unicos:
                    artistas_unicos[artist] = ArtistClass.Artist(artistsTree.convertAscii(artistID), artist)
                artistList.append(artistas_unicos[artist]) #Lista de artistas de una cancion como objetos

    #---------------------------------------------------------------------------------------------------------------
                # Se genera el árbol de artistas
                artistsTree.generateArtistsTree(artistas_unicos[artist])

            # Se obtiene toda la información relevante de la canción
            songID = jsonPlaylist[i]['items'][j]['track']['id']
            songName = jsonPlaylist[i]['items'][j]['track']['name']
            songDuration = jsonPlaylist[i]['items'][j]['track']['duration_ms']
            songPopularity = jsonPlaylist[i]['items'][j]['track']['popularity']
            # Se genera el árbol de canciones
            songsTree.generateSongsTree(songsTree.convertAscii(songID), songName, artistList, songDuration, songPopularity)
    """
    print("\nCanciones: ")

    print("\nÁrbol en Preorden:")
    songsTree.pre_order(songsTree.root)
    """
    print("\nArtistas: ")

    print("\nÁrbol en Preorden:")
    artistsTree.pre_order(artistsTree.root)