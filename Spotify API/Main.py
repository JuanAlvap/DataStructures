import AVL
import Procedimientos
import ArtistClass
import json
import API
from TreeVisualizer import AVLTreeVisualizer

songsTree = AVL.AVLTree()
popularityTree = AVL.AVLTree()
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
if len(jsonPlaylist) == 1:
    if int(jsonPlaylist[0]['error']['status']) == 404:
        print("Playlist no encontrada")
        print("Digite un playlist correcta")
        print(len(jsonPlaylist))
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

                # Se valida que haya información en cada casilla y asi evitar errores
                if jsonPlaylist[i]['items'][j]['track']['artists'][k]['name'] == None or jsonPlaylist[i]['items'][j]['track']['artists'][k]['id'] == None:
                    continue
                artist = jsonPlaylist[i]['items'][j]['track']['artists'][k]['name']
                artistID = jsonPlaylist[i]['items'][j]['track']['artists'][k]['id']
                if artist not in artistas_unicos:
                    artistas_unicos[artist] = ArtistClass.Artist(artistsTree.convertAscii(artistID), artist)
                artistList.append(artistas_unicos[artist]) #Lista de artistas de una cancion como objetos
            
    #---------------------------------------------------------------------------------------------------------------
                # Se genera el árbol de artistas
                artistsTree.generateArtistsTree(artistas_unicos[artist])

            # Se valida que haya información en cada casilla y asi evitar errores
            if (jsonPlaylist[i]['items'][j]['track']['id'] == None or jsonPlaylist[i]['items'][j]['track']['name'] == None 
            or jsonPlaylist[i]['items'][j]['track']['duration_ms'] == None or jsonPlaylist[i]['items'][j]['track']['popularity'] == None):
                continue

            # Se obtiene toda la información relevante de la canción
            songID = jsonPlaylist[i]['items'][j]['track']['id']
            songName = jsonPlaylist[i]['items'][j]['track']['name']
            songDuration = jsonPlaylist[i]['items'][j]['track']['duration_ms']
            songPopularity = jsonPlaylist[i]['items'][j]['track']['popularity']
            # Se genera el árbol de canciones
            songsTree.generateSongsTree(songsTree.convertAscii(songID), songName, artistList, songDuration, songPopularity, popularityTree)


"""
    print("\nCanciones: ")

    print("\nÁrbol en Preorden:")
    songsTree.pre_order(songsTree.root)
    
    print("\nArtistas: ")

    print("\nÁrbol en Preorden:")
    artistsTree.pre_order(artistsTree.root)
"""

print()
process = Procedimientos.Process()
artista_mas_popular = process.artista_con_mas_canciones(songsTree)
print(f"El artista con más canciones es: {artista_mas_popular}")
print()
artistaMayorPopularidad = process.artista_mas_popular(songsTree)
print(f"El artista con mayor popularidad es: {artistaMayorPopularidad}")
print()
nivelesMayorPopularidad = process.mostrar_niveles_mayor_popularidad(songsTree)
print(f"El artista con mayor popularidad {artistaMayorPopularidad} tiene sus canciones en los niveles {nivelesMayorPopularidad}")
print()
alturaSongs, alturaArtists = process.alturas(songsTree, artistsTree)
print(f"la altura del árbol de canciones es {alturaSongs}, La altura del árbol de artistas es {alturaArtists}")
print()
print(f"El número de rotaciones necesarias a la hora de construir el árbol de canciones es {process.rotacionesSongs(songsTree)}")
print()
cancionesMayores = process.cancionesConDuracionMayorAlPromedio(songsTree.root)
print(f"Las canciones con duración mayor al promedio son {cancionesMayores}")
print()
artistaBuscado = "Bad Bunny"
cancionesArtista = process.canciones_artista(songsTree, artistsTree, artistaBuscado)
print(f"Las canciones del artista {artistaBuscado} son {cancionesArtista}")
print()
# Imprimir el árbol en preorden
#print("\nÁrbol de popularidad en Preorden:")
#popularityTree.pre_order(popularityTree.root)
print()
N = 8
print(f"Las {N} canciones más populares son")
lista_canciones = process.obtener_n_canciones_populares(popularityTree, N)
    
# Ahora 'lista_canciones' contendrá las 5 canciones de mayor popularidad en la playlist.
for cancion in lista_canciones:
    print(cancion)

visualizerArtistas = AVLTreeVisualizer(artistsTree, False, False)
visualizerArtistas.render("AVL1")
visualizerCanciones = AVLTreeVisualizer(songsTree, True, True)
visualizerCanciones.render("AVL2")
visualizerPopularity = AVLTreeVisualizer(popularityTree, True, True)
visualizerPopularity.render("AVL3")