import Halma
import Heuristics
import DecisionTree


class NormalMinMax:
    movesTable = []

    def __init__(self, game, player, heuristic):
        self.decisionTree = DecisionTree.DecisionTree(game, player, heuristic)

    def playOneGame(self):
        hasEnded = False
        iteration = 1
        winner = ""
        while not hasEnded:
            print(f"Iteration: {iteration}")
            iteration += 1
            self.decisionTree.makeDecisionTree(2)
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
        (game, _, _, children) = node
        if node != self.decisionTree.tree:
            self.movesTable.append(game)
        if game.winner != "None" or children == []:
            return

        node = children[0]
        maxValue = 0
        for child in children:
            (_, heuristic2, _, children) = child
            if heuristic2 > maxValue:
                node = child
                maxValue = heuristic2

        self.makeDecisionRecursion(node, DecisionTree.oppositePlayer(player))

    def printMoves(self):
        prevGameBoard = Halma.Halma()
        for move, game in enumerate(self.movesTable):
            if move != 0:
                print(f"Move nr {move}")
                print(f"Player 1 pieces: {len(game.player1)}")
                print(f"Player 2 pieces: {len(game.player2)}")
                game.printBoardDiff(prevGameBoard)
            prevGameBoard = game.getBoard()
            print("\n")


class AlfaBetaMinMax:
    movesTable = []

    def __init__(self, game, player, heuristic):
        self.decisionTree = DecisionTree.DecisionTree(game, player, heuristic)

    def playOneGame(self):
        hasEnded = False
        iteration = 1
        winner = ""
        while not hasEnded:
            print(f"Iteration: {iteration}")
            iteration += 1
            if iteration == 200:
                break
            self.decisionTree.makeDecisionTree(2)
            self.makeDecision()
            game = self.movesTable[len(self.movesTable)-1]
            if game.winner != "None":
                hasEnded = True
                winner = game.winner
            self.decisionTree.tree = (game, 0, [float('-inf'), float('inf')], [])
        self.printMoves()
        print(f"{winner} has won!")

    def makeDecision(self):
        self.makeDecisionRecursion(self.decisionTree.tree, self.decisionTree.player)
        (game, _, _, chldrn) = self.decisionTree.tree
        children = chldrn
        #self.movesTable.append(game)
        while children != []:
            (game, _, _, chldrn2) = children[0]
            self.movesTable.append(game)
            children = chldrn2
        #(game, _, _, chldrn2) = children[0]
        #self.movesTable.append(game)

    def makeDecisionRecursion(self, node, player):
        (game, heuristic, alfabeta, children) = node
        if game.winner != "None" or children == []:
            return heuristic
        if player == self.decisionTree.player:  # max here
            maxValue = float('-inf')
            maxNode = None
            for child in children:
                value = self.makeDecisionRecursion(child, DecisionTree.oppositePlayer(player))
                if value > maxValue:
                    maxValue = value
                    maxNode = child
                if alfabeta[1] <= alfabeta[0]:
                    break
            children[0] = maxNode
            return maxValue
        else:                                   # min here
            minValue = float('inf')
            minNode = None
            for child in children:
                value = self.makeDecisionRecursion(child, DecisionTree.oppositePlayer(player))
                if value < minValue:
                    minValue = value
                    minNode = child
                if alfabeta[1] <= alfabeta[0]:
                    break
            children[0] = minNode
            return minValue

    def printMoves(self):
        for move, game in enumerate(self.movesTable):
            print(f"Move nr {move}")
            game.printBoard()
            print("\n")
