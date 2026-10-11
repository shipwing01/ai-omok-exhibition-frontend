def get_next_move(game_state):
    # 보드에서 현재 돌의 위치를 확인합니다.
    board = game_state["board"]

    # 가운데가 비어 있으면 첫 수로 선택합니다.
    if board[9][9] == 0:
        return {"x": 9, "y": 9}

    # 가운데를 사용할 수 없다면 위쪽 행부터 첫 빈칸을 찾습니다.
    for y in range(19):
        for x in range(19):
            if board[y][x] == 0:
                return {"x": x, "y": y}

    # 바둑판에 빈칸이 없으면 둘 수 없음을 알립니다.
    raise ValueError("바둑판에 빈칸이 없습니다.")
