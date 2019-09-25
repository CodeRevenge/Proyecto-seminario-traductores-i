from src.crearContLoc import ContadorLocalidades

class Relativos(ContadorLocalidades):
    def __init__(self):
        ContadorLocalidades.__init__(self)

        self.RELATIVO = 'REL'
        self.RELATIVO_9 = 'REL9'

        self.direccionesRelativos = []
        self.direccionesRelativos9 = []

    def esRelativo(self, nemonico):
        return True if nemonico[2] == self.RELATIVO or nemonico[2] == self.RELATIVO_9 else False