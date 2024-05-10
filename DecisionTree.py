import Halma
import Heuristics


def oppositePlayer(player):
    return 1 if player == 2 else 2


class DecisionTree:

    def __init__(self, game, player, heuristic):
        self.game = game
        self.player = player
        self.tree = (game, 0, [float('-inf'), float('inf')], [])
        self.heuristic = heuristic
        self.currIteration = 0

    def makeDecisionTree(self, iterations):
        self.currIteration = 0
        self.continueDecisionTree(self.tree, self.player, iterations)

    def continueDecisionTree(self, node, player, iterationsLeft):

        if iterationsLeft == 0:
            return
        (game, _, _, everyMovePossible) = node
        if game.winner != "None":
            return
        everyMoveTemp = []
        for piece in game.getPlayer(player):
            moves = game.movesOptions(piece)
            for move in moves["Move"]:
                everyMoveTemp.append((piece, move))
            for jump in moves["Jump"]:
                everyMoveTemp.append((piece, jump))

        for move in everyMoveTemp:
            (piece, destination) = move
            (pl1, pl2) = game.movePieceReturnCopy(piece, destination)
            afterMove = Halma.Halma()
            afterMove.setAll(pl1, pl2)
            afterMove.checkIfEnded()
            everyMovePossible.append((afterMove, self.heuristic(afterMove.player1,
                                                                 afterMove.player2),
                                                  [float('-inf'), float('inf')], []))

        iterationsLeft -= 1

        for move in everyMovePossible:
            self.continueDecisionTree(move, oppositePlayer(player), iterationsLeft)
        return

    def printTree(self):
        self.printNode(self.tree, 0)

    def printNode(self, node, level):
        (game, _, _, children) = node

        if game.winner != "None":
            print(f"Winner is {game.winner}")
        print(f"\nNode level {level}:")
        game.printBoard()

        for child in children:
            self.printNode(child, level + 1) if child else []
