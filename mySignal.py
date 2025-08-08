class SignalSended():
    def __init__(self, type, roomID, data=None):
        self.type = type #wait, fire, createroom, joinroom
        self.roomID = roomID
        self.data = data

    def __str__(self):
        return str(self.type) + " " + str(self.roomID) + " " + str(self.listShip) + " " + str(self.posFire)
    
class SignalRecieved():
    def __init__(self, phase, type=None, turnIP=None, playerIP=None, data=None):
        self.phase = phase
        self.type = type
        self.turnIP = turnIP
        self.playerIP = playerIP
        self.data = data

    def __str__(self):
        return str(self.phase) + " " + str(self.turnIP) + " " + str(self.playerIP) #+ " " + str(self.posFire)