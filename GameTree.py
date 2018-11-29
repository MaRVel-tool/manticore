from manticore.ethereum import ManticoreEVM

class GameTree(object):
    def __init__(self, parent=None, state=None):
        self.parent = parent
        self.manticore_state = state
