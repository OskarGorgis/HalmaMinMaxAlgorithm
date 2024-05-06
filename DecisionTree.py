import Halma
import Heuristics


def oppositePlayer(player):
    return 1 if player == 2 else 2


class DecisionTree:

    def __init__(self, game, player, heuristic): #TODO przetrzymywanie tylko informacji i położeniu graczy
        self.game = game
        self.player = player
        self.tree = (game, (0, 0, 0), [])
        self.heuristic = heuristic

    def makeDecisionTree(self, iterations):
        self.continueDecisionTree(self.tree, self.player, iterations)

    def continueDecisionTree(self, node, player, iterationsLeft):
        if iterationsLeft == 0:
            return
        (game, _, everyMovePossible) = node
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
            (board, pl1, pl2) = game.movePieceReturnCopy(piece, destination)
            afterMove = Halma.Halma()
            afterMove.setAll(board, pl1, pl2)
            afterMove.checkIfEnded()
            everyMovePossible.append((afterMove, (self.heuristic(afterMove.board,
                                                                 True if player == 1 else False,
                                                                 afterMove.getPlayer(player)), 0, 0), []))

        iterationsLeft -= 1

        for move in everyMovePossible:
            self.continueDecisionTree(move, oppositePlayer(player), iterationsLeft)
        return

    def printTree(self):
        self.printNode(self.tree, 0)

    def printNode(self, node, level):
        (game, _, children) = node

        if game.winner != "None":
            print(f"\nNode level {level}:")
            print(f"Winner is {game.winner}")
            game.printBoard()
        for child in children:
            self.printNode(child, level + 1) if child else []
