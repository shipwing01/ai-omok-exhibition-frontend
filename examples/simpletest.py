def get_next_move(game_state):
    board = game_state["board"]

    for y in range(19):
        for x in range(19):
            if board[y][x] == 0:
                return {"x": x, "y": y}

    return None
