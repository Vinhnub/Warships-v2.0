
class Player():
    def __init__(self, name, network):
        self.name = name
        self.network = network
        self.data = None
    
    def setData(self, newData):
        self.data = newData

    