import Heuristics


class Halma:
    player1 = []
    player2 = []
    winner = "None"

    def __init__(self):
        self.board = [[0 for _ in range(16)] for _ in range(16)]
        self.isEnded = False

    def setAll(self, board, player1, player2):
        self.board = board
        self.player1 = player1
        self.player2 = player2

    def printBoard(self):
        for x in self.board:
            print(x)

    def movesOptions(self, piece):
        (pieceX, pieceY) = piece
        if self.board[pieceX][pieceY] == 0:
            print("Sprawdzanie ruchu pustego pola")
            return {"Move": [], "Jump": []}
        possibleMoves = {"Move": [], "Jump": []}
        pieceType = self.board[pieceX][pieceY]
        for x in [pieceX - 1, pieceX, pieceX + 1]:
            for y in [pieceY - 1, pieceY, pieceY + 1]:
                if 0 <= x < 16 and 0 <= y < 16 and not (pieceX == x and pieceY == y):
                    if self.board[x][y] == 0:
                        possibleMoves["Move"].append((x, y))
                    elif self.board[x][y] != pieceType:
                        possibleMoves["Jump"] = possibleMoves["Jump"] + \
                                                self.checkForJumps(pieceX, pieceY, pieceType, set())
        return possibleMoves

    def checkForJumps(self, pieceX, pieceY, pieceType, forbiddenFields):
        possibleJumps = []
        enemyPiece = 1 if pieceType == 2 else 2
        for x in [pieceX - 1, pieceX, pieceX + 1]:
            for y in [pieceY - 1, pieceY, pieceY + 1]:
                if 0 <= x < 16 and 0 <= y < 16 and not (pieceX == x and pieceY == y):
                    if self.board[x][y] == enemyPiece:
                        newX = x + (x - pieceX)
                        newY = y + (y - pieceY)
                        if 16 > newX >= 0 == self.board[newX][newY] and 0 <= newY < 16 and (
                                (newX, newY) not in forbiddenFields):
                            possibleJumps.append((newX, newY))
                            forbiddenFields.add((newX, newY))
                            possibleJumps = possibleJumps + self.checkForJumps(newX, newY, pieceType, forbiddenFields)
        return possibleJumps

    def movePiece(self, start, end):
        (xs, ys) = start
        (xe, ye) = end
        if self.board[xs][ys] == 0:
            print("Próba ruchu z pustego pola")
        elif self.board[xe][ye] != 0:
            print("Próba ruchu na zajęte pole")
        else:
            self.board[xe][ye] = self.board[xs][ys]
            self.board[xs][ys] = 0
            if self.board[xe][ye] == 1:
                self.player1.remove((xs, ys))
                self.player1.append((xe, ye))
            if self.board[xe][ye] == 2:
                self.player2.remove((xs, ys))
                self.player2.append((xe, ye))

    def movePieceReturnCopy(self, start, end):
        (xs, ys) = start
        (xe, ye) = end
        if self.board[xs][ys] == 0:
            print("Próba ruchu z pustego pola")
        elif self.board[xe][ye] != 0:
            print("Próba ruchu na zajęte pole")
        else:
            newBoard = list(range(16))
            for i in range(len(self.board)):
                newBoard[i] = self.board[i].copy()
            newPlayer1 = self.player1.copy()
            newPlayer2 = self.player2.copy()
            newBoard[xe][ye] = newBoard[xs][ys]
            newBoard[xs][ys] = 0
            if newBoard[xe][ye] == 1:
                newPlayer1.remove((xs, ys))
                newPlayer1.append((xe, ye))
            if newBoard[xe][ye] == 2:
                newPlayer2.remove((xs, ys))
                newPlayer2.append((xe, ye))
            return newBoard, newPlayer1, newPlayer2

    def checkIfEnded(self):
        if Heuristics.baseHeuristic(False, self.player1) == 570:  # powinno być True
            self.winner = "Player 1"
        elif Heuristics.baseHeuristic(False, self.player2) == 570:
            self.winner = "Player 2"

    def loadBoard(self, boardToLoad):
        if len(boardToLoad) != 16:
            print("Błędna wielkość tablicy")
        else:
            isValid = True
            for x in range(16):
                if len(boardToLoad[x]) != 16:
                    isValid = False
            if not isValid:
                print("Błędna wielkość tablicy")
            else:
                for i in range(len(boardToLoad)):
                    for j in range(len(boardToLoad[i])):
                        if boardToLoad[i][j] == 1:
                            self.player1.append((i, j))
                        elif boardToLoad[i][j] == 2:
                            self.player2.append((i, j))
                self.board = boardToLoad

    def setBoard(self, board):
        self.board = board

    def getBoard(self):
        return self.board

    def printBoard(self):
        for line in self.board:
            print(line)

    def getPlayer(self, player):
        return self.player1 if player == 1 else self.player2
