class OnlineGame:
    def __init__(self, id):
        self.end = False
        self.p1Move = False
        self.p2Move = False
        self.winner = False
        self.id = id
        self.ready = 0
        self.colorWent = 'white'
