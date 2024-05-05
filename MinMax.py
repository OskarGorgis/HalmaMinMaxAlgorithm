import Heuristics
import DecisionTree


class NormalMinMax:
    movesTable = []

    def __init__(self, game, player):
        self.decisionTree = DecisionTree.DecisionTree(game, player, Heuristics.mixHeuristic)

    def playOneGame(self):
        hasEnded = False
        iteration = 1
        winner = ""
        while not hasEnded:
            print(f"Iteration: {iteration}")
            iteration += 1
            self.decisionTree.makeDecisionTree(4)
            self.makeDecision()
            game = self.movesTable[len(self.movesTable)-1]
            if game.winner != "None":
                hasEnded = True
                winner = game.winner
            self.decisionTree.tree = (game, (0, 0, 0), [])
        self.printMoves()
        print(f"{winner} has won!")

    def makeDecision(self):
        self.makeDecisionRecursion(self.decisionTree.tree, self.decisionTree.player)
        # self.printMoves()

    def makeDecisionRecursion(self, node, player):
        (game, (heuristic, _, _), children) = node
        self.movesTable.append(game)
        if game.winner != "None" or children == []:
            return

        node = children[0]
        maxValue = 0
        for child in children:
            (_, (heuristic2, _, _), children) = child
            if heuristic2 > maxValue:
                node = child
                maxValue = heuristic2

        self.makeDecisionRecursion(node, DecisionTree.oppositePlayer(player))

    def printMoves(self):
        for move, game in enumerate(self.movesTable):
            print(f"Move nr {move}")
            game.printBoard()
            print("\n")
