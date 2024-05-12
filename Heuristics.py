def didWin(playerPieces, rightTopCorner):
    value = 0
    if rightTopCorner:
        base = {(0, 11), (0, 12), (0, 13), (0, 14), (0, 15), (1, 11), (1, 12), (1, 13), (1, 14), (1, 15), (2, 12),
                (2, 13), (2, 14), (2, 15), (3, 13), (3, 14), (3, 15), (4, 14), (4, 15)}
    else:
        base = {(15, 0), (15, 1), (15, 2), (15, 3), (15, 4), (14, 0), (14, 1), (14, 2), (14, 3), (14, 4), (13, 0),
                     (13, 1), (13, 2), (13, 3), (12, 0), (12, 1), (12, 2), (11, 0), (11, 1)}
    for piece in playerPieces:
        if piece in base:
            value += 1
    return value == 19


def distanceHeuristic(playerPieces, enemyPieces):
    value = 0
    x, y = 0, 15
    ex, ey = 15, 0
    for (i, j) in playerPieces:
        value -= abs(i-x) + abs(j-y)
    for (i, j) in enemyPieces:
        value += abs(i-ex) + abs(j-ey)
    return value

def baseHeuristic(playerPieces, enemyPieces):
    value = 0
    base = {(0, 11), (0, 12), (0, 13), (0, 14), (0, 15), (1, 11), (1, 12), (1, 13), (1, 14), (1, 15), (2, 12),
            (2, 13), (2, 14), (2, 15), (3, 13), (3, 14), (3, 15), (4, 14), (4, 15)}
    enemyBase = {(15, 0), (15, 1), (15, 2), (15, 3), (15, 4), (14, 0), (14, 1), (14, 2), (14, 3), (14, 4), (13, 0),
            (13, 1), (13, 2), (13, 3), (12, 0), (12, 1), (12, 2), (11, 0), (11, 1)}
    for piece in playerPieces:
        value += 30 if piece in base else 0
    for piece in enemyPieces:
        value -= 30 if piece in enemyBase else 0
    return value


def mixHeuristic(playerPieces, enemyPieces):
    value1 = 0
    value2 = 0
    base = {(0, 11), (0, 12), (0, 13), (0, 14), (0, 15), (1, 11), (1, 12), (1, 13), (1, 14), (1, 15), (2, 12),
            (2, 13), (2, 14), (2, 15), (3, 13), (3, 14), (3, 15), (4, 14), (4, 15)}
    x, y = 0, 15
    enemyBase = {(15, 0), (15, 1), (15, 2), (15, 3), (15, 4), (14, 0), (14, 1), (14, 2), (14, 3), (14, 4), (13, 0),
            (13, 1), (13, 2), (13, 3), (12, 0), (12, 1), (12, 2), (11, 0), (11, 1)}
    ex, ey = 15, 0
    for (i, j) in playerPieces:
        value1 += 30 if (i, j) in base else 0
        value2 += abs(i - x) + abs(j - y)
    for (i, j) in enemyPieces:
        value1 -= 30 if (i, j) in enemyBase else 0
        value2 -= abs(i - ex) + abs(j - ey)
    return value1 + value2


def clusteringHeuristic(playerPieces, enemyPieces):
    value = 0
    for i, (px, py) in enumerate(playerPieces):
        for j, (qx, qy) in enumerate(playerPieces):
            if i != j:
                value -= abs(px - qx) + abs(py - qy)
    for i, (px, py) in enumerate(enemyPieces):
        for j, (qx, qy) in enumerate(enemyPieces):
            if i != j:
                value += abs(px - qx) + abs(py - qy)
    value = value/19
    x, y = 0, 15
    ex, ey = 15, 0
    for (i, j) in playerPieces:
        value -= (abs(i - x) + abs(j - y)) * 3
    for (i, j) in enemyPieces:
        value += (abs(i - ex) + abs(j - ey)) * 3

    return value


def strategicPositionHeuristic(playerPieces, enemyPieces):
    value = 0
    strategic_points = [(5, 5), (10, 10), (5, 10), (10, 5)]

    for (px, py) in playerPieces:
        value += sum(4 - (abs(px - sx) + abs(py - sy)) for (sx, sy) in strategic_points)

    for (ex, ey) in enemyPieces:
        value -= sum(4 - (abs(ex - sx) + abs(ey - sy)) for (sx, sy) in strategic_points)

    x, y = 0, 15
    ex, ey = 15, 0
    for (i, j) in playerPieces:
        value -= (abs(i - x) + abs(j - y)) * 5
    for (i, j) in enemyPieces:
        value += (abs(i - ex) + abs(j - ey)) * 5

    return value


def baseDefenseHeuristic(playerPieces, enemyPieces):
    value = 0
    player_base = {(0, 11), (0, 12), (0, 13), (0, 14), (0, 15), (1, 11), (1, 12), (1, 13), (1, 14), (1, 15), (2, 12),
            (2, 13), (2, 14), (2, 15), (3, 13), (3, 14), (3, 15), (4, 14), (4, 15)}
    enemyBase = {(15, 0), (15, 1), (15, 2), (15, 3), (15, 4), (14, 0), (14, 1), (14, 2), (14, 3), (14, 4), (13, 0),
                 (13, 1), (13, 2), (13, 3), (12, 0), (12, 1), (12, 2), (11, 0), (11, 1)}

    for (px, py) in playerPieces:
        if (px, py) in player_base:
            value += 2
    for (px, py) in enemyPieces:
        if (px, py) in player_base:
            value -= 2

    for (px, py) in enemyPieces:
        if (px, py) in enemyBase:
            value -= 2
    for (px, py) in playerPieces:
        if (px, py) in enemyBase:
            value += 2

    x, y = 0, 15
    ex, ey = 15, 0
    for (i, j) in playerPieces:
        value -= abs(i - x) + abs(j - y)
    for (i, j) in enemyPieces:
        value += abs(i - ex) + abs(j - ey)

    return value

