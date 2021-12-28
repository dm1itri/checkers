class OnlineGame:
    def __init__(self, board, id):
        self.end = False
        self.p1Went = False
        self.p2Went = False
        self.id = id
        self.ready = 0
        self.board = board
        self.colorWent = 'white'
