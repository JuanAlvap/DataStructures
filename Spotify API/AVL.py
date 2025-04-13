import CancionClass
import ArtistClass
import json
class AVLTree:
    def __init__(self):
        self.root = None

    def addNode(self, root, new_node):
        if root is None:
            return new_node
        
        if root.uniqueID == new_node.uniqueID:
            #print("El elemento ya está")
            return root
        
        if new_node.uniqueID > root.uniqueID:
            root.right = self.addNode(root.right, new_node)
        else:
            root.left = self.addNode(root.left, new_node)
        
        root.balance = self.height(root.left) - self.height(root.right)
        
        if root.balance == 2:
            if root.left.balance == -1:
                root.left = self.rotate_right(root.left)
            return self.rotate_left(root)
        
        if root.balance == -2:
            if root.right.balance == 1:
                root.right = self.rotate_left(root.right)
            return self.rotate_right(root)
        
        return root
    
    def rotate_right(self, node):
        aux = node.right
        node.right = aux.left
        aux.left = node
        aux.balance = self.height(aux.left) - self.height(aux.right)
        node.balance = self.height(node.left) - self.height(node.right)
        return aux
    
    def rotate_left(self, node):
        aux = node.left
        node.left = aux.right
        aux.right = node
        aux.balance = self.height(aux.left) - self.height(aux.right)
        node.balance = self.height(node.left) - self.height(node.right)
        return aux
    
    def height(self, node):
        if node is None:
            return 0
        return 1 + max(self.height(node.left), self.height(node.right))
    
    def pre_order(self, node):
        if node is not None:
            print(node)
            self.pre_order(node.left)
            self.pre_order(node.right)
    
    def generateSongsTree(self, id, name, artistas, duracion, popularidad):
        new_node = CancionClass.Cancion(id, name, artistas, duracion, popularidad)
        if self.root is None:
            self.root = new_node
            print(f"La raíz ha sido añadida {new_node.uniqueID}")
        else:
            self.root = self.addNode(self.root, new_node)
            

    def generateArtistsTree(self, artist):
        if self.root is None:
            self.root = artist
            print(f"La raíz ha sido añadida {artist.uniqueID}")
        else:
            self.root = self.addNode(self.root, artist)
    
    def convertAscii(self, string):
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