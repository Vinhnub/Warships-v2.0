class SignalSended():
    def __init__(self, type=None, roomID=None, data=None, anotherData=None):
        self.type = type #wait, fire, createroom, joinroom
        self.roomID = roomID
        self.data = data
        self.anotherData = data

    def __str__(self):
        return str(self.type) + " " + str(self.roomID) + " " + str(self.data) 
    
class SignalRecieved():
    def __init__(self, phase=None, type=None, turnIP=None, playerIP=None, data=None, coolDown=None):
        self.phase = phase
        self.type = type
        self.turnIP = turnIP
        self.playerIP = playerIP
        self.data = data
        self.coolDown = coolDown

    def __str__(self):
        return str(self.phase) + " " + str(self.type) + " " +  str(self.turnIP) + " " + str(self.playerIP) + " " + str(self.data) + " " + str(self.coolDown)