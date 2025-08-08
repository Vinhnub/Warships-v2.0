class SignalSended():
    def __init__(self, type, roomID, listShip=None, posFire=None):
        self.type = type #wait, fire, createroom, joinroom
        self.roomID = roomID
        self.listShip = listShip
        self.posFire = posFire

    def __str__(self):
        return str(self.type) + " " + str(self.roomID) + " " + str(self.listShip) + " " + str(self.posFire)
    
class SignalRecieved():
    def __init__(self, phase, type=None, turnIP=None, playerIP=None):
        self.phase = phase
        self.type = type
        self.turnIP = turnIP
        self.playerIP = playerIP

    def __str__(self):
        return str(self.phase) + " " + str(self.turnIP) + " " + str(self.playerIP) #+ " " + str(self.posFire)