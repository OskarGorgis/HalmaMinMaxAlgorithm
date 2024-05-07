

def draw_game_changes(arr1, arr2):
    if len(arr1) != 16 or len(arr2) != 16 or len(arr1[0]) != 16 or len(arr2[0]) != 16:
        print("Ostrzeżenie: Jedna lub obie tablice nie mają wymiarów 16x16")
        return

    differences = []
    for i in range(16):
        for j in range(16):
            if arr1[i][j] != arr2[i][j]:
                differences.append((i, j, arr1[i][j], arr2[i][j]))
                print(f"Różnica w pozycji ({i}, {j}): {arr1[i][j]} != {arr2[i][j]}")