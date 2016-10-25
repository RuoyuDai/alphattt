# -*- coding: UTF-8 -*-
from client.player import Player
from client.board import Board
import time
from player import rand_ai
from client.client import run

class MctsQw(Player):
    def __init__(self, cal_time, board):
        self.cur_opponent_state = board.start()
        self.cur_opponent_move = None
        self.board = board
        self.mcts = Pybot(cal_time, self.board)
    
    def update(self, move, game_state):
        if move != None:
            self.cur_opponent_state = self.board.next_state(self.cur_opponent_state, move)
        
    def display(self, game_state):
        self.board.display(game_state)
        
    def get_move(self):
        self.mcts.get_move(self.cur_opponent_state)

class Pybot(object):
    def __init__(self, cal_time, board):
        super(Pybot, self).__init__()
        self.tree = {}
        self.cal_time = cal_time
        self.board = board

    def __random_choice(self, legal_moves, _):
        return rand_ai.choice(legal_moves)

    def __choice(self, legal_moves, state):
        return self.__random_choice(legal_moves, state)

    def get_move(self, state):
        paras = {"begin": time.time(), "num": 0, "time": 0}
        legal_moves = self.board.legal_moves(state)
        if len(legal_moves) == 0:
            return None
        expect_winner = self.board.next_player(state)
        while True:
            paras["num"] += 1
            self.__inc_tree(self.__tree_path(state, legal_moves), expect_winner)
            paras["time"] = time.time() - paras["begin"]
            if paras["time"] > self.cal_time:
                break
        msg_time = "== calculate %d paths using %f seconds ==" % (paras["num"], paras["time"])
        move, msg_pro = self.__search_tree(state, legal_moves)
        print msg_time, msg_pro
        return move

    def __tree_path(self, state, legal_moves):
        _state = list(state)
        _legal_moves = legal_moves
        move_trace = []
        while True:
            _state = self.board.next_state(_state, self.__choice(_legal_moves, _state))
            winner = self.board.winner(_state)
            move_trace.append(tuple(_state))
            if winner is not None:
                return (move_trace, winner)
            _legal_moves = self.board.legal_moves(_state)

    def __inc_tree(self, (move_trace, winner), expect_winner):
        inc = {"win": 0, "total": 1}
        if winner == expect_winner:
            inc["win"] = 1
        for item in move_trace:
            node = None
            try:
                node = self.tree[item]
            except Exception:
                self.tree[item] = {"win": 0, "total": 0, "per": 0}
                node = self.tree[item]
            node["win"] += inc["win"]
            node["total"] += inc["total"]
            node["per"] = node["win"] / node["total"]

    def __search_node(self, state, move):
        _state = list(state)
        node = self.tree.get(tuple(self.board.next_state(_state, move)), None)
        return node

    def __search_tree(self, state, legal_moves):
        final = {"per": 0, "win": 0, "total": 0, "move": None}
        for move in legal_moves:
            node = self.__search_node(state, move)
            if node is None:
                continue
            wins = node["win"] * 100 / node["total"]
            if wins >= final["per"]:
                final["per"], final["win"], final["total"], final["move"] = \
                    wins, node["win"], node["total"], move
        msg_pro = "== probability is %d. %d/%d ==" % (final["per"], final["win"], final["total"])
        # print msg_pro
        return final["move"], msg_pro

if __name__ == '__main__':
    run(MctsQw, "127.0.0.1", 8011, "kk", "123456", 8)
