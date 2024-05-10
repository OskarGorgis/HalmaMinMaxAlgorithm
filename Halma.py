import HalmaAI
import Heuristics


class Halma:
    player1 = []
    player2 = []
    winner = "None"

    def __init__(self):
        self.isEnded = False

    def setAll(self, player1, player2):
        self.player1 = player1
        self.player2 = player2

    def movesOptions(self, piece):
        (pieceX, pieceY) = piece
        if piece not in self.player1 and piece not in self.player2:
            print("Sprawdzanie ruchu pustego pola")
            return {"Move": [], "Jump": []}
        possibleMoves = {"Move": [], "Jump": []}
        pieceType = 1 if piece in self.player1 else 2
        for x in [pieceX - 1, pieceX, pieceX + 1]:
            for y in [pieceY - 1, pieceY, pieceY + 1]:
                if 0 <= x < 16 and 0 <= y < 16 and not (pieceX == x and pieceY == y):
                    if (x, y) not in self.player1 and (x, y) not in self.player2:
                        possibleMoves["Move"].append((x, y))
                    elif (1 if (x, y) in self.player1 else 2) != pieceType:
                        possibleMoves["Jump"] = possibleMoves["Jump"] + \
                                                self.checkForJumps(pieceX, pieceY, pieceType, set())
        return possibleMoves

    def checkForJumps(self, pieceX, pieceY, pieceType, forbiddenFields):
        possibleJumps = []
        enemyPiece = 1 if pieceType == 2 else 2
        for x in [pieceX - 1, pieceX, pieceX + 1]:
            for y in [pieceY - 1, pieceY, pieceY + 1]:
                if 0 <= x < 16 and 0 <= y < 16 and not (pieceX == x and pieceY == y):
                    if (x, y) in self.player1:
                        currPiece = 1
                    elif (x, y) in self.player2:
                        currPiece = 2
                    else:
                        currPiece = 0
                    if currPiece == enemyPiece:
                        newX = x + (x - pieceX)
                        newY = y + (y - pieceY)
                        if (16 > newX >= 0 and 0 <= newY < 16 and (
                                (newX, newY) not in forbiddenFields) and (newX, newY) not in self.player1
                                and (newX, newY) not in self.player2):
                            possibleJumps.append((newX, newY))
                            forbiddenFields.add((newX, newY))
                            possibleJumps = possibleJumps + self.checkForJumps(newX, newY, pieceType, forbiddenFields)
        return possibleJumps

    def movePiece(self, start, end):
        if start not in self.player1 and start not in self.player2:
            print("Próba ruchu z pustego pola")
        elif end in self.player1 or end in self.player2:
            print("Próba ruchu na zajęte pole")
        else:
            if start in self.player1:
                self.player1.remove(start)
                self.player1.append(end)
            else:
                self.player2.remove(start)
                self.player2.append(end)

    def movePieceReturnCopy(self, start, end):
        if start not in self.player1 and start not in self.player2:
            print("Próba ruchu z pustego pola")
        elif end in self.player1 or end in self.player2:
            print(f"Próba ruchu z pola {start} na zajęte pole {end}")
        else:
            newPlayer1 = self.player1.copy()
            newPlayer2 = self.player2.copy()
            if start in self.player1:
                newPlayer1.remove(start)
                newPlayer1.append(end)
            else:
                newPlayer2.remove(start)
                newPlayer2.append(end)
            return newPlayer1, newPlayer2

    def checkIfEnded(self):
        if Heuristics.didWin(self.player1, True) == 570:
            self.winner = "Player 1"
        elif Heuristics.didWin(self.player2, False) == 570:
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

    def getBoard(self):
        board = [[0 for _ in range(16)] for _ in range(16)]
        for (x, y) in self.player1:
            board[x][y] = 1
        for (x, y) in self.player2:
            board[x][y] = 2
        return board

    def printBoardDiff(self, basicBoard):
        board = [[0 for _ in range(16)] for _ in range(16)]
        for (x, y) in self.player1:
             board[x][y] = 1
        for (x, y) in self.player2:
            board[x][y] = 2
        print()
        for line in board:
            print(line)
        HalmaAI.draw_game_changes(basicBoard, board)

    def printBoard(self):
        board = [[0 for _ in range(16)] for _ in range(16)]
        for (x, y) in self.player1:
             board[x][y] = 1
        for (x, y) in self.player2:
            board[x][y] = 2
        for line in board:
            print(line)

    def getPlayer(self, player):
        return self.player1 if player == 1 else self.player2
