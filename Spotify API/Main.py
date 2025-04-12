import AVL
import json


songsTree = AVL.AVLTree()
artistsTree = AVL.AVLTree()
# Función para convertir el id del artista a numeros con ayuda del ASCII
def convertAscii(string):
    ascii = ""
    # Se carga el archivo JSON que contiene los valores en ASCII de cada letra
    with open('asciiTable.json', 'r', encoding='utf-8') as file:
        asciiFile = json.load(file)
    # Se recorre el string, se obtiene el valor de cada letra en ascii y se concatena a un string
    for i in range(len(string)):
        numero = int(asciiFile[string[i]])
        ascii += str(numero)

    # Se convierte el string en un numero entero y se retorna como id
    numAscii = int(ascii)
    return numAscii


with open('playlist.json', 'r', encoding='utf-8') as jsonFile:
    # Se carga el archivo JSON que contiene la información de la playlist
    jsonPlaylist = json.load(jsonFile)

    # Se recorre la lista de respuestas en JSON y se obtiene el id de la playlist
for i in range(len(jsonPlaylist)):
    for j in range(len(jsonPlaylist[i]['items'])):
        artistList = []
        for k in range(len(jsonPlaylist[i]['items'][j]['track']['artists'])):
            artists = jsonPlaylist[i]['items'][j]['track']['artists'][k]['name']
            artistList.append(artists)

#---------------------------------------------------------------------------------------------------------------

            artistID = jsonPlaylist[i]['items'][j]['track']['artists'][k]['id']
            artistsTree.generateArtistsTree(convertAscii(artistID), artists)

        songID = jsonPlaylist[i]['items'][j]['track']['id']
        songName = jsonPlaylist[i]['items'][j]['track']['name']
        songDuration = jsonPlaylist[i]['items'][j]['track']['duration_ms']
        songPopularity = jsonPlaylist[i]['items'][j]['track']['popularity']
        songsTree.generateSongsTree(convertAscii(songID), songName, artistList, songDuration, songPopularity)
"""
print("\nCanciones: ")

print("\nÁrbol en Preorden:")
songsTree.pre_order(songsTree.root)
"""
print("\nArtistas: ")

print("\nÁrbol en Preorden:")
artistsTree.pre_order(artistsTree.root)