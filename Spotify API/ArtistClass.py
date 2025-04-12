class Artist:
    _id_counter = 1  # Atributo estático para el ID único
    
    def __init__(self, uniqueID: int, name: str):
        self.uniqueID = uniqueID
        self.name = name
        self.ID = Artist._id_counter
        self.left = None
        self.right = None
        self.balance = 0
        Artist._id_counter += 1  # Incrementar el contador para el siguiente artista
    
    def __str__(self):
        return f"{self.ID}: {self.uniqueID}, {self.name}"