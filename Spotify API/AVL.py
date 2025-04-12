import CancionClass
import ArtistClass

class AVLTree:
    def __init__(self):
        self.root = None

    def addNode(self, root, new_node):
        if root is None:
            return new_node
        
        if root.uniqueID == new_node.uniqueID:
            print("El elemento ya está")
            return root
        
        if new_node.ID > root.ID:
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
            print(f"La raíz ha sido añadida {new_node.ID}")
        else:
            self.root = self.addNode(self.root, new_node)
            

    def generateArtistsTree(self, ID, name):
        new_node = ArtistClass.Artist(ID, name)
        if self.root is None:
            self.root = new_node
            print(f"La raíz ha sido añadida {new_node.ID}")
        else:
            self.root = self.addNode(self.root, new_node)