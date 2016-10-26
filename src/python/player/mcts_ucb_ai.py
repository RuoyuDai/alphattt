# -*- coding: UTF-8 -*-
import time
from client.client import run, Player
import random

class MctsAI(Player):
    def __init__(self, cal_time, board):
        super(MctsAI, self).__init__(cal_time, board)
        self.tree = {}

    def get_move(self):
        legal_game_state = self.player_legal_states(self.cur_opponent_state)
        if len(legal_game_state) == 1:
            return legal_game_state[0]
        games, max_depth, spent_time = self.run_simulation(legal_game_state)
        print "Simulate [%d] games, using [%f] seconds, max depth [%d] ==" % (games, spent_time, max_depth)
        move_stats = self.make_state(legal_game_state)
        return self.choose_best(move_stats)
    
    def run_simulation(self, legal_game_state):
        expect_winner = self.board.next_player(self.cur_opponent_state)
        begin_time, games, max_depth, spent_time = time.time(), 0, 0, 0
        while True:
            expand, need_update, new_depth, winner = self.random_game(legal_game_state, max_depth)
            self.propagate_back(expand, need_update, expect_winner, winner)
            max_depth = max(max_depth, new_depth)
            spent_time = time.time() - begin_time
            games += 1
            if spent_time > self.cal_time:
                break
        return games, max_depth, spent_time

    def random_game(self, legal_game_state, max_depth):
        expand, need_update, iter_count = [], [], 1
        while True:
            state = self.select_one(legal_game_state)
            winner = self.board.winner(state)
            if winner is not None:
                return expand, need_update, max_depth, winner
            if self.tree.has_key(state):
                need_update.append(state)
            elif len(expand) == 0:
                expand.append(state)
                max_depth = iter_count
            iter_count += 1
            legal_game_state = self.player_legal_states(state)

    def propagate_back(self, expand, need_update, expect_winner, winner):
        for expand_state in expand:
            self.tree[expand_state] = {"win": 0, "total": 0, "per": 0}
            need_update.append(expand_state)
        win = 1 if winner == expect_winner else 0
        for update_state in need_update:
            node = self.tree[update_state]
            node["win"] += win
            node["total"] += 1
            node["per"] = node["win"] / node["total"]
    
    def select_one(self, legal_game_state):
        return random.choice(legal_game_state)[1]
    
    def make_state(self, legal_game_state):
        return [(move, self.get_per(self.tree.get(state, None))) for move, state in legal_game_state]
        
    def get_per(self, node):
        return node["per"] if node is not None else -1
            
    def choose_best(self, move_stats):
        return max(move_stats, lambda x : x(1))[0]

    def player_legal_states(self, state):
        legal_moves = self.board.legal_moves(state)
        that = self
        legal_states = map(
            lambda move: that.board.next_state(state, move),
            legal_moves)
        return list(zip(legal_moves, legal_states))

    def choice(self, legal_moves, state):
        return self.random.choice(legal_moves)

if __name__ == '__main__':
    run("127.0.0.1", 8011, "TT", "123456", 3, MctsAI)
