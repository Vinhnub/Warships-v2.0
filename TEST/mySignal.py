class Signal():
    def __init__(self, data):
        self.data = data

    def setData(self, newData):
        self.data = newData

    def __str__(self):
        return str(self.data)