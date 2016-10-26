# -*- coding: UTF-8 -*-
from client.board import Board


def run(player1_cls, player2_cls, count):
    cal_time, board = 0.1, Board()
    player1 = player1_cls(cal_time, board)
    player2 = player2_cls(cal_time, board)
    i = 0
    player1_win_count = 0;
    player2_win_count = 0;
    while i < count:
        winner = one_game(board, player1, player2)
        i++
        player1_win_count = player1_win_count + 1 if winner == player1.__class__ else player1_win_count
        player2_win_count = player2_win_count + 1 if winner == player2.__class__ else player2_win_count
        
        
def one_game(board, player1, player2):
    state = board.start()
    move = None
    winner = None
    while True:
        state, move, winner = one_step(state, move, board, player1)
        if move == None:
            break;
        state, move, winner = one_step(state, move, board, player2)
        if move == None:
            break;
    return winner
    
def one_step(state, move, board, player):
    player.update(move, state)
    move = player.get_move()
    state = board.next_state(state, move)
    if board.winner(state) is not None:
        print player.__class__, "win"
        return None, None, player.__class__
    return state, move
if __name__ == '__main__':
    pass