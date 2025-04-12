class Cancion:
    _id_counter = 1  # Atributo estático para el ID único
    
    def __init__(self, uniqueID: int, name: str, artists: list, duracion: int, popularidad: int):
        self.uniqueID = uniqueID
        self.name = name
        self.artists = artists
        self.duracion = duracion  # En segundos
        self.popularidad = popularidad  # De 0 a 100
        self.ID = Cancion._id_counter
        self.left = None
        self.right = None
        self.balance = 0
        Cancion._id_counter += 1  # Incrementar el contador para la siguiente canción
    
    def __str__(self):
        return f"{self.ID}: {self.name} - {', '.join(self.artists)} ({self.duracion}s, Popularidad: {self.popularidad})"
    
    def getUniqueID(self):
        return self.uniqueID
