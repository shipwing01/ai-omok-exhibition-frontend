BOARD_SIZE = 19
DIRECTIONS = ((1, 0), (0, 1), (1, 1), (1, -1))


def wins_at(board, x, y, stone):
    # 이 빈칸에 돌을 두었을 때 오목이 되는지 검사합니다.
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
        board[y][x] = 0


def line_score(board, x, y, stone):
    # 가상의 착수 뒤 이어지는 돌의 수와 양쪽 끝의 열린 정도를 점수로 만듭니다.
    board[y][x] = stone
    score = 0
    try:
        for dx, dy in DIRECTIONS:
            count = 1
            open_ends = 0

            for sign in (-1, 1):
                nx = x + dx * sign
                ny = y + dy * sign
                while 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE and board[ny][nx] == stone:
                    count += 1
                    nx += dx * sign
                    ny += dy * sign
                if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE and board[ny][nx] == 0:
                    open_ends += 1

            # 돌이 길게 이어지고 양쪽이 열려 있을수록 높은 점수를 줍니다.
            if count >= 5:
                score += 100000
            elif count == 4:
                score += 12000 if open_ends == 2 else 6000
            elif count == 3:
                score += 1800 if open_ends == 2 else 350
            elif count == 2:
                score += 250 if open_ends == 2 else 60
            else:
                score += 25 if open_ends == 2 else 5
    finally:
        board[y][x] = 0
    return score


def get_next_move(game_state):
    # 내 돌과 상대 돌의 번호를 확인합니다.
    board = game_state["board"]
    my_stone = game_state["myStone"]
    opponent = 3 - my_stone
    empty_cells = []

    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            if board[y][x] == 0:
                empty_cells.append((x, y))

    if not empty_cells:
        raise ValueError("바둑판에 빈칸이 없습니다.")

    # 승리할 수 있는 수와 상대의 승리 수 차단을 점수 평가보다 먼저 처리합니다.
    for x, y in empty_cells:
        if wins_at(board, x, y, my_stone):
            return {"x": x, "y": y}
    for x, y in empty_cells:
        if wins_at(board, x, y, opponent):
            return {"x": x, "y": y}

    best_move = None
    best_score = None
    for x, y in empty_cells:
        # 내 연결은 키우고 상대 연결도 막도록 공격과 수비를 함께 계산합니다.
        attack = line_score(board, x, y, my_stone)
        defense = line_score(board, x, y, opponent)
        center_bonus = 18 - abs(x - 9) - abs(y - 9)
        score = attack + defense * 0.9 + center_bonus
        if best_score is None or score > best_score:
            best_move = {"x": x, "y": y}
            best_score = score

    return best_move
