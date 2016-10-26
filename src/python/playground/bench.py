# -*- coding: UTF-8 -*-
from client.board import Board
from player.mcts_ai import MctsAI
from player.rand_ai import RandomAI


def run(player1_cls, player2_cls, count):
    cal_time, board = 0.1, Board()
    player1 = player1_cls(cal_time, board)
    player2 = player2_cls(cal_time, board)
    i = 0
    player1_win_count = 0;
    player2_win_count = 0;
    while i < count:
        winner = one_game(board, player1, player2)
        i += 1
        player1_win_count = player1_win_count + 1 if winner == player1.__class__ else player1_win_count
        player2_win_count = player2_win_count + 1 if winner == player2.__class__ else player2_win_count
    player1_win_rate = player1_win_count / count
    player2_win_rate = player2_win_count / count
    print "played %d games, "%count,  player1.__class__ \
        ," win %d(%f)," %(player1_win_count, player1_win_rate),\
        player2.__class__, " win %d(%f),"%(player2_win_count, player2_win_rate)   
        
def one_game(board, player1, player2):
    state = board.start()
    move = None
    winner = None
    while True:
        state, move, winner = one_step(state, move, board, player1, 1)
        board.display(state)
        if move == None:
            print winner, "win"
            break
        state, move, winner = one_step(state, move, board, player2, 2)
        board.display(state)
        if move == None:
            print winner, "win"
            break
    return winner
    
def one_step(state, move, board, player, winner):
    player.update(move, state)
    move = player.get_move()
    print player.__class__, move
    state = board.next_state(state, move)
    if board.winner(state) == winner:
        return state, None, player.__class__
    if board.winner(state) == Board.DRAW:
        return state, None, None
    return state, move, None

if __name__ == '__main__':
    run(RandomAI, MctsAI, 1)
