import AVL
import json
import ArtistClass

songsTree = AVL.AVLTree()
artistsTree = AVL.AVLTree()

with open('playlist.json', 'r', encoding='utf-8') as jsonFile:
    # Se carga el archivo JSON que contiene la información de la playlist
    jsonPlaylist = json.load(jsonFile)

    # Se recorre la lista de respuestas en JSON y se obtiene el id de la playlist
artistas_unicos = {} #lista de artistas totales del árbol como objetos
for i in range(len(jsonPlaylist)):
    for j in range(len(jsonPlaylist[i]['items'])):
        artistList = []
        for k in range(len(jsonPlaylist[i]['items'][j]['track']['artists'])):
            artist = jsonPlaylist[i]['items'][j]['track']['artists'][k]['name']
            artistID = jsonPlaylist[i]['items'][j]['track']['artists'][k]['id']
            if artist not in artistas_unicos:
                artistas_unicos[artist] = ArtistClass.Artist(artistsTree.convertAscii(artistID), artist)
            artistList.append(artistas_unicos[artist]) #Lista de artistas de una cancion como objetos

#---------------------------------------------------------------------------------------------------------------
            artistsTree.generateArtistsTree(artistas_unicos[artist])

        songID = jsonPlaylist[i]['items'][j]['track']['id']
        songName = jsonPlaylist[i]['items'][j]['track']['name']
        songDuration = jsonPlaylist[i]['items'][j]['track']['duration_ms']
        songPopularity = jsonPlaylist[i]['items'][j]['track']['popularity']
        songsTree.generateSongsTree(songsTree.convertAscii(songID), songName, artistList, songDuration, songPopularity)
"""
print("\nCanciones: ")

print("\nÁrbol en Preorden:")
songsTree.pre_order(songsTree.root)
"""
print("\nArtistas: ")

print("\nÁrbol en Preorden:")
artistsTree.pre_order(artistsTree.root)