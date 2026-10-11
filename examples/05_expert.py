BOARD_SIZE = 19
DIRECTIONS = ((1, 0), (0, 1), (1, 1), (1, -1))


def wins_at(board, x, y, stone):
    # 이 칸에 돌을 둔 뒤 다섯 개가 이어지는지 네 방향으로 확인합니다.
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


def placement_score(board, x, y, stone):
    # 네 방향의 연속 길이, 열린 끝, 오목이 될 수 있는 다섯 칸 구간을 함께 평가합니다.
    board[y][x] = stone
    total = 0
    active_directions = 0
    try:
        opponent = 3 - stone
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

            # 열린 끝이 많은 긴 연결은 상대가 막기 어렵기 때문에 더 높게 평가합니다.
            if count >= 5:
                direction_score = 1000000
            elif count == 4:
                direction_score = 30000 if open_ends == 2 else 14000
            elif count == 3:
                direction_score = 3500 if open_ends == 2 else 700
            elif count == 2:
                direction_score = 500 if open_ends == 2 else 100
            else:
                direction_score = 35 if open_ends == 2 else 8

            # 착수가 포함된 다섯 칸 구간에서 상대 돌이 없고 빈칸이 남았는지 봅니다.
            best_window = 0
            window_has_three = False
            for start in range(-4, 1):
                own_count = 0
                empty_count = 0
                blocked = False
                for offset in range(start, start + 5):
                    nx = x + dx * offset
                    ny = y + dy * offset
                    if not (0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE):
                        blocked = True
                        break
                    value = board[ny][nx]
                    if value == opponent:
                        blocked = True
                        break
                    if value == stone:
                        own_count += 1
                    else:
                        empty_count += 1

                if blocked:
                    continue
                if own_count == 5:
                    window_score = 1000000
                elif own_count == 4:
                    window_score = 18000 if empty_count == 1 else 0
                elif own_count == 3:
                    window_score = 2200 if empty_count == 2 else 600
                elif own_count == 2:
                    window_score = 280 if empty_count == 3 else 70
                else:
                    window_score = 20 if empty_count == 4 else 0
                best_window = max(best_window, window_score)
                if own_count >= 3:
                    window_has_three = True

            total += direction_score + best_window
            if count >= 3 or window_has_three:
                active_directions += 1

        # 여러 방향에서 동시에 연결 기회가 생기는 수를 추가로 높게 평가합니다.
        if active_directions >= 3:
            total += 50000
        elif active_directions == 2:
            total += 18000
    finally:
        board[y][x] = 0
    return total


def candidate_cells(board):
    # 돌 주변 두 칸 안의 빈자리만 후보로 삼아 불필요한 먼 수를 줄입니다.
    candidates = []
    has_stone = False
    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            if board[y][x] != 0:
                has_stone = True
                continue
            near_stone = False
            for ny in range(max(0, y - 2), min(BOARD_SIZE, y + 3)):
                for nx in range(max(0, x - 2), min(BOARD_SIZE, x + 3)):
                    if board[ny][nx] != 0:
                        near_stone = True
                        break
                if near_stone:
                    break
            if near_stone:
                candidates.append((x, y))

    if not has_stone and board[9][9] == 0:
        return [(9, 9)]
    if candidates:
        return candidates

    # 주변 후보가 없으면 남은 모든 빈칸을 살펴봅니다.
    return [
        (x, y)
        for y in range(BOARD_SIZE)
        for x in range(BOARD_SIZE)
        if board[y][x] == 0
    ]


def get_next_move(game_state):
    # 내 돌과 상대 돌을 정하고, 실제로 둘 수 있는 후보만 만듭니다.
    board = game_state["board"]
    my_stone = game_state["myStone"]
    opponent = 3 - my_stone
    candidates = candidate_cells(board)

    if not candidates:
        raise ValueError("바둑판에 빈칸이 없습니다.")

    # 즉시 이기는 수와 즉시 패배를 막는 수는 복합 점수보다 우선합니다.
    for x, y in candidates:
        if wins_at(board, x, y, my_stone):
            return {"x": x, "y": y}
    for x, y in candidates:
        if wins_at(board, x, y, opponent):
            return {"x": x, "y": y}

    best_move = None
    best_score = None
    for x, y in candidates:
        # 공격과 수비를 함께 계산하고, 중앙에 가까운 자리에는 작은 보너스를 줍니다.
        attack = placement_score(board, x, y, my_stone)
        defense = placement_score(board, x, y, opponent)
        center_bonus = 18 - abs(x - 9) - abs(y - 9)
        score = attack + defense * 0.95 + center_bonus
        if best_score is None or score > best_score:
            best_move = {"x": x, "y": y}
            best_score = score

    return best_move
