from manticore.ethereum import ManticoreEVM

class GameTree(object):
    def __init__(self, m, c):
        self.manticore = m
        self.contract = c

    def get_functions(self):
        return self.contract._hashes

