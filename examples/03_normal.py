BOARD_SIZE = 19
DIRECTIONS = ((1, 0), (0, 1), (1, 1), (1, -1))


def wins_at(board, x, y, stone):
    # 가상의 돌을 둔 뒤 네 방향 중 한 곳이라도 다섯 개가 이어지는지 봅니다.
    board[y][x] = stone
    try:
        for dx, dy in DIRECTIONS:
            count = 1
            for sign in (-1, 1):
                nx = x + dx * sign
                ny = y + dy * sign
                while 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE and board[ny][nx] == stone:
                    count += 1
                    nx += dx * sign
                    ny += dy * sign
            if count >= 5:
                return True
        return False
    finally:
        # 실제 보드 상태가 바뀌지 않도록 가상의 돌을 되돌립니다.
        board[y][x] = 0


def get_next_move(game_state):
    # 흑은 1, 백은 2이고 상대 돌은 나머지 숫자입니다.
    board = game_state["board"]
    my_stone = game_state["myStone"]
    opponent = 3 - my_stone
    empty_cells = []

    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            if board[y][x] == 0:
                empty_cells.append((x, y))

    # 빈칸이 없으면 유효한 착수를 만들 수 없습니다.
    if not empty_cells:
        raise ValueError("바둑판에 빈칸이 없습니다.")

    # 이 수로 다섯 개를 완성할 수 있으면 가장 먼저 둡니다.
    for x, y in empty_cells:
        if wins_at(board, x, y, my_stone):
            return {"x": x, "y": y}

    # 상대가 다음 수에 이길 수 있는 빈칸을 먼저 막습니다.
    for x, y in empty_cells:
        if wins_at(board, x, y, opponent):
            return {"x": x, "y": y}

    # 당장 이기거나 막을 수 없으면 가운데에 가까운 빈칸을 둡니다.
    best_x, best_y = empty_cells[0]
    best_distance = (best_x - 9) ** 2 + (best_y - 9) ** 2
    for x, y in empty_cells[1:]:
        distance = (x - 9) ** 2 + (y - 9) ** 2
        if distance < best_distance:
            best_x, best_y = x, y
            best_distance = distance

    return {"x": best_x, "y": best_y}
