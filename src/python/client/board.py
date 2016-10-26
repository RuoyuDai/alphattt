# -*- coding: UTF-8 -*-


class Board(object):
    PlAYER_1_WIN = 1
    PLAYER_2_WIN = 2
    DRAW = 3
    ON_GOING = 4
    
    game_state = [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, None, None, 1 ]
    posValue = [1, 2, 4, 8, 16, 32, 64, 128, 256]
    wins = [1 + 2 + 4, 8 + 16 + 32, 64 + 128 + 256, 1 + 8 + 64, 2 + 16 + 128, 4 + 32 + 256,
            1 + 16 + 256, 4 + 16 + 64]
    lineIndex2grid = {0 : 2, 1 : 4,2 : 6,3 : 9,4 : 11,5 : 13,6 : 16,7 : 18,8 : 20}
    #player1_pos = {0, 2, 4, 6, 8, 10, 12, 14, 16}
    #player2_pos = {1, 3, 5, 7, 9, 11, 13, 15, 17}
    #girdIndex = {(0, 0) : 0}

    def start(self): 
        return list(self.game_state)

    def next_state(self, state, move):
        res = list(state) 
        player = res[22]
        gridIndex = (move[0] * 3 + move[1]) * 2 - 1 + player
        gridValue = self.posValue[move[2] * 3 + move[3]]
        res[gridIndex] = res[gridIndex] + gridValue
        res[18] = self.judgeBigWin(1, res)
        res[19] = self.judgeBigWin(2, res)
        res[20] = move[2]
        res[21] = move[3]
        res[22] = 3 - player
        return res
    
    def judgeBigWin(self, player, state):
        res = 0;
        for i in range(0, 9):
            if(self.isWin(state[i*2 + player - 1])):
                res += self.posValue[i]
        return res
    

    def currentPlayer(self, state):
        return state[22]
    
    def legal_moves(self, state):
        bGridX = state[20]
        bGridY = state[21]
        if (type(bGridX) is not int or type(bGridY) is not int):
            return self.findAllLegal(state)

        gridIndex = (bGridX * 3 + bGridY) * 2 - 1
        player1GirdValue = state[gridIndex + 1]
        player2GridValue = state[gridIndex + 2]
        if (self.isWin(player1GirdValue) or self.isWin(player2GridValue) or self.isGridFull(player1GirdValue + player2GridValue)) :
            return self.findAllLegal(state)

        return self.findGirdLegalMoves(state[gridIndex + 1], state[gridIndex + 2], bGridX, bGridY)

    def max_moves(self):
        return 81;
    
    def winner(self, state):
        if(self.isWin(state[18])):
            return self.PlAYER_1_WIN
        
        if(self.isWin(state[19])):
            return self.PLAYER_2_WIN
        
        if(self.isFull(state)):
            return self.DRAW
        
        return self.ON_GOING
    
    def isFull(self, state):
        for i in range(0, 9):
            total = state[i*2] + state[i*2 + 1];
            if((not self.isGridFull(total)) and (not self.isWin(state[i*2])) and (not self.isWin(state[i*2 + 1]))):
                return False;
        return True;
    
    def isGridFull(self, i):
        return i == 511;

    def findGirdLegalMoves(self, player1value, player2value, gridx, gridy):
        res = []
        total = player1value + player2value;
        for i in range(0, 9):
            if ((total & self.posValue[i]) == 0):
                res.append([gridx, gridy, i / 3, i % 3 ])
        return res;

    def findAllLegal(self, state):
        res = []
        for i in range(0, 9):
            player1GirdValue = state[i*2];
            player2GridValue = state[i*2 + 1];
            if (self.isWin(player1GirdValue) or self.isWin(player2GridValue) or self.isGridFull(player1GirdValue + player2GridValue)):
                continue
            tmp = self.findGirdLegalMoves(player1GirdValue, player2GridValue, i / 3, i % 3);
            res += tmp
        return res

    def isWin(self, i):
        for win in self.wins:
            if ((i & win) == win):
                return True;
        return False;

    def display(self, state):
        wholeGrid = [[0 for x in range(0, 9)] for x in range(0, 9)]
        for i in range(0, 9):
            grid = self.parseGrid(state[2 * i], state[2 * i + 1]);
            self.copyGrid(wholeGrid, grid, i);

        for line in range(0, len(wholeGrid)):
            if (line % 3 == 0):
                self.displayBorder();
            self.displayOneLine(wholeGrid[line]);
        self.displayBorder();

    def copyGrid(self, wholeGrid, grid, i):
        offsetX = (i / 3) * 3;
        offsetY = (i % 3) * 3;
        for xi in range(0, 3):
            for yi in range(0, 3):
                wholeGrid[xi + offsetX][yi + offsetY] = grid[xi][yi]

    def parseGrid(self, player1, player2):
        res = [[0, 0, 0 ], [ 0, 0, 0 ], [ 0, 0, 0 ]]
        for i in range(len(self.posValue) - 1, -1, -1):
            player1 = self.matchStep(player1, self.posValue[i], i, 1, res);
            player2 = self.matchStep(player2, self.posValue[i], i, 2, res);
        return res

    def matchStep(self, player, value, pos, desc, res):
        if (player / value > 0) :
            player = player - value;
            res[pos / 3][pos % 3] = desc;
        return player;

    def displayOneLine(self, line):
        s = list("||     ||     ||     ||")
        for i in range(0, len(line)):
            if (line[i] == 1):
                s[self.lineIndex2grid.get(i)] = 'x';
            elif (line[i] == 2):
                s[self.lineIndex2grid.get(i)] = 'o';
        print "".join(s)

    def displayBorder(self):
        print("----------------------")
