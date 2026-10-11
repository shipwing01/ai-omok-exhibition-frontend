def get_next_move(game_state):
    # 보드에서 현재 돌의 위치를 확인합니다.
    board = game_state["board"]
    best_move = None
    best_distance = None

    # 가운데(9, 9)와 거리가 가장 가까운 빈칸을 찾습니다.
    for y in range(19):
        for x in range(19):
            if board[y][x] != 0:
                continue

            # 제곱 거리를 사용하면 제곱근 계산 없이 가까운 칸을 비교할 수 있습니다.
            distance = (x - 9) ** 2 + (y - 9) ** 2
            if best_distance is None or distance < best_distance:
                best_move = {"x": x, "y": y}
                best_distance = distance

    if best_move is not None:
        return best_move

    # 둘 수 있는 빈칸이 없으면 잘못된 좌표 대신 상황을 알립니다.
    raise ValueError("바둑판에 빈칸이 없습니다.")
