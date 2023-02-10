import re


class Chess: 
    """ Chess board as dictionaries """

    def __init__(self, moves = [], count = 0):
        
        # History of moves in order <piece> <start position> <end position>
        self.moves = moves
        
        # Moves counter
        self.count = count

        # Generate coordinates
        self.coordinates()

        # Initiates board
        self.board_init()
        
        # Initiates starting positions on board
        self.setup()

        # Main players combat
        self.game()
        
        # Print notation
        self.print_notation()
    
    # self._board is a dict where keys is coordinate type string and values is piece type object ( e.g. king is object of King())
    @property
    def board(self):
        return self._board
    
    @board.setter
    def board(self, board):
        self._board = board

    @property
    def count(self):
        return self._count
    
    @count.setter
    def count(self, count):
        self._count = count
    
    @property
    def moves(self):
        return self._moves
    
    @moves.setter
    def moves(self, moves):
        self._moves = moves

    @property
    def coordinates_list(self):
        return self._coordinates_list
    
    @coordinates_list.setter
    def coordinates_list(self, coordinates_list):
        self._coordinates_list = coordinates_list

    def coordinates(self):
        """
        Create list of two digit string name coordinate_list
        save listin self.coordinate_list
        first digit is letter from a to h
        second digit is number frim 1 to 8
        e.g. d6
        
        :return: A list of string coordinates
        :rtype: list
        """
        coordinates_list = []
        for i in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']:
            for j in range(1, 9):
                coordinates_list.append(i + str(j))
        self.coordinates_list = coordinates_list           

    def board_init(self):
        """
        Create chess board
        keys coordinates from coordinates_list

        :return: A dict
        :rtype: dict
        """
        self.board = dict.fromkeys(self.coordinates_list)

    def setup(self):
        """
        Set up chess board
        """

        # Setup white pieces
        self.board['e1'] = self.King('white')
        self.board['d1'] = self.Queen('white')
        for pos in ['a1', 'h1']:
            self.board[pos] = self.Rook('white')
        for pos in ['c1', 'f1']:
            self.board[pos] = self.Bishop('white')
        for pos in ['b1', 'g1']:
            self.board[pos] = self.Knight('white')
        for pos in ['a2', 'b2', 'c2', 'd2', 'e2', 'f2', 'g2', 'h2']:
            self.board[pos] = self.Pawn('white')

        # Setup black pieces
        self.board['e8'] = self.King('black')
        self.board['d8'] = self.Queen('black')
        for pos in ['a8', 'h8']:
            self.board[pos] = self.Rook('black')
        for pos in ['c8', 'f8']:
            self.board[pos] = self.Bishop('black')
        for pos in ['b8', 'g8']:
            self.board[pos] = self.Knight('black')
        for pos in ['a7', 'b7', 'c7', 'd7', 'e7', 'f7', 'g7', 'h7']:
            self.board[pos] = self.Pawn('black')

    def print_board(self):
        # Print upper line with alphabetic coordinate
        print('  ', end = '')
        for i in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']:
            print(f' {i} ', end = '')
        print('  ')

        # Print board with piece and numeric coordinate
        for j in range(8, 0, -1):
            print(f' {j}', end = '')
            for k in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']:
                pos = k + str(j)
                if self.board[pos] == None:
                    print('   ', end='')
                else:
                    print(f' {self.board[pos]} ', end = '')
            print(f' {j}')

        # Print lower line with alphabetic coordinate
        print('  ', end = '')
        for i in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']:
            print(f' {i} ', end = '')
        print('  ')

    def team_round(self):
        if self.count % 2 == 0:
            team = 'white'
        else:
            team = 'black'
        return team

    def prompt(self):

        # Team tracking
        team = self.team_round()

        # Checking player order to move
        # Accept only: <piece> <start position> <end position>. e.g. king e1 f2
        try:
            # end game by exit commend
            prompt = input(f"{team} move: ")
            if prompt == 'exit':
                return 'exit'
            piece, start, end = prompt.lower().split()
        except:
            print("Invalid order")
            print("Usage: <piece> <start position> <end position> e.g. pawn a2 a4")
            return 1

        # Accept only correct piece name
        if piece not in ['king', 'queen', 'rook', 'bishop', 'knight',  'pawn']:
            print(f"{piece} is not chess piece\nUsage: king, queen, rook, bishop, knight, pawn")
            return 1
        
        # Accept only correct coordinate
        match = re.search("[a-h][1-8]", start)
        if not match:
            print(f"{match} is not chess coordinate\nUsage: [a-h][1-8] e.g. f6")
            return 1
        
        # Accept only correct coordinate
        match = re.search("[a-h][1-8]", end)
        if not match:
            print(f"{match} is not chess coordinate\nUsage: [a-h][1-8] e.g. f6")
            return 1
        
        if self.board[start] == None:
            print(f"There is no {piece} in here")
            return 1

        if self.board[start] == self.board[end]:
            print('Start square can not be the same as end square')
            return 1

        # Accept only current team pieces
        if not self.board[start].team == team:
            print(f"This {piece} is not yours")
            return 1
        
        # Move piece with correct name
        if not self.board[start].character == piece:
            print(f"{piece} is not in {start}")
            return 1
        
        return [piece, start, end, team]

    def move(self):
        
        prompt = self.prompt()
        if prompt == 'exit':
            return 'exit'
        
        if prompt == 1:
            return
        
        piece, start, end, team = prompt

        posibility_moves, posibility_takens = self.board[start].ability(start, self.board, team)
        if end in posibility_moves:
            step = self.board[start]
            self.board[end] = step
            self.board[start] = None
            
            # Add move to history
            stage = f'{piece} {start} {end}'
            self.moves.append(stage)
            self.count += 1
        elif end in posibility_takens:
            step = self.board[start]
            self.board[end] = step
            self.board[start] = None
            
            # Add move to history
            stage = f'{piece} {start} {end}'
            self.moves.append(stage)
            self.count += 1
        else:
            print(f'{piece} can not do that for you')
            return 1
        

    def game(self):
        while True:
            self.print_board()
            if self.move() == 'exit':
                break
    
    def print_notation(self):
        if self.moves == []:
            print('No moves')
        else:
            for line in self.moves:
                print(line)


    class Piece:
        def __init__(self, team, character):
            self.team = team
            self.character = character
        
        def __str__(self):
            return f'{self.team} {self.character}'
        
        @property
        def team(self):
            return self._team
        
        @team.setter
        def team(self, team):
            if team not in ['white', 'black']:
                raise ValueError('Invalid team')
            self._team = team
        
        @property
        def character(self):
            return self._character
        
        @character.setter
        def character(self, character):
            if character not in ['king', 'queen', 'rook', 'bishop', 'knight', 'pawn']:
                raise ValueError('Invalid character')
            self._character = character
        
        def convert_to_numeric(self, pos):
            num = ord(pos[0]) - 96
            return [num, int(pos[1])]
        
        def convert_to_alpha(self, pos):
            alpha = chr(int(pos[0]) + 96)
            return alpha + str(pos[1])
        
        def sum_coordinates(self, pos1, pos2):
            pos3 = []
            pos3.append(pos1[0] + pos2[0])
            pos3.append(pos1[1] + pos2[1])
            return pos3
        
        def is_it_in_board(self, pos_numeric):
            if pos_numeric[0] > 0:
                if pos_numeric[0] < 9:
                    if pos_numeric[1] > 0:
                        if pos_numeric[1] < 9:
                            return True
            return False
        
        def posible_moves(self, start, board, team, deltas, mrange):
            
            start_numeric = self.convert_to_numeric(start)
            moves = []
            takens = []
            for delta in deltas:
                step = [None, None]
                step[0] = int(delta[0])
                step[1] = int(delta[1])
                copy_mrange = mrange
                while True and copy_mrange != 0:
                    #piece range
                    copy_mrange = mrange - 1
                    # move one step
                    posible_position = self.sum_coordinates(start_numeric, step)

                    # step for next iteration
                    step[0] = step[0] + delta[0]
                    step[1] = step[1] + delta[1]

                    # check is it in board
                    if self.is_it_in_board(posible_position):
                        pass
                    else:
                        break
                    # check is it None
                    if board[self.convert_to_alpha(posible_position)] == None:
                        moves.append(posible_position)  
                    elif not board[self.convert_to_alpha(posible_position)].team == team:
                        takens.append(posible_position)
                        break
                    else:
                        break
            
            alpha_moves = []
            for move in moves:
                alpha_moves.append(self.convert_to_alpha(move))
            
            alpha_takens = []
            for taken in takens:
                alpha_takens.append(self.convert_to_alpha(taken))
            
            return alpha_moves, alpha_takens


    class King(Piece):
        def __init__(self, team, character = 'king'):
            super().__init__(team, character)
        
        def __str__(self):
            if self.team == 'white':
                return f'♔'
            else:
                return f'♚'

        def ability(self, start, board, team):
            deltas = [[1, 1], [0, 1], [-1, 1], [-1, 0], [-1, -1], [0, -1], [1, -1], [1, 0]]       
            mrange = 1
            alpha_moves, alpha_takens = self.posible_moves(start, board, team, deltas, mrange)

            return alpha_moves, alpha_takens


    class Queen(Piece):
        def __init__(self, team, character = 'queen'):
            super().__init__(team, character)
        
        def __str__(self):
            if self.team == 'white':
                return f'♕'
            else:
                return f'♛'
        
        def ability(self, start, board, team):
            deltas = [[1, 1], [0, 1], [-1, 1], [-1, 0], [-1, -1], [0, -1], [1, -1], [1, 0]]       
            mrange = 8
            alpha_moves, alpha_takens = self.posible_moves(start, board, team, deltas, mrange)

            return alpha_moves, alpha_takens


    class Rook(Piece):
        def __init__(self, team, character = 'rook'):
            super().__init__(team, character)
        
        def __str__(self):
            if self.team == 'white':
                return f'♖'
            else:
                return f'♜'
        
        def ability(self, start, board, team):
            deltas = [[0, 1], [-1, 0], [0, -1], [1, 0]]       
            mrange = 8
            alpha_moves, alpha_takens = self.posible_moves(start, board, team, deltas, mrange)

            return alpha_moves, alpha_takens


    class Bishop(Piece):
        def __init__(self, team, character = 'bishop'):
            super().__init__(team, character)
        
        def __str__(self):
            if self.team == 'white':
                return f'♗'
            else:
                return f'♝'
        
        def ability(self, start, board, team):
            deltas = [[1, 1], [1, -1], [-1, 1], [-1, -1]]       
            mrange = 8
            alpha_moves, alpha_takens = self.posible_moves(start, board, team, deltas, mrange)
            return alpha_moves, alpha_takens


    class Knight(Piece):
        def __init__(self, team, character = 'knight'):
            super().__init__(team, character)
        
        def __str__(self):
            if self.team == 'white':
                return f'♘'
            else:
                return f'♞'

        def ability(self, start, board, team):
            deltas = [[1, 2], [2, 1], [2, -1], [1, -2], [-1, -2], [-2, -1], [-2, 1], [-1, 2]]
            mrange = 1
            alpha_moves, alpha_takens = self.posible_moves(start, board, team, deltas, mrange)

            return alpha_moves, alpha_takens


    class Pawn(Piece):
        
        def __init__(self, team, character = 'pawn'):
            super().__init__(team, character)

            self.turn = 0
        
        def __str__(self):
            if self.team == 'white':
                return f'♙'
            else:
                return f'♟'
        
        @property
        def turn(self):
            return self._turn
        
        @turn.setter
        def turn(self, turn):
            self._turn = turn
        
        def posible_taken(self, start, board, team):
            
            start_numeric = self.convert_to_numeric(start)
            takens = []
            if team == 'white':
                deltas = [[-1, 1], [1, 1]]
            else:
                deltas = [[1, -1], [-1, -1]]
            
            for delta in deltas:
                posible_taken = self.sum_coordinates(start_numeric, delta)
                
                # check is it in board
                if self.is_it_in_board(posible_taken):
                    # Check is it empty square
                    if not board[self.convert_to_alpha(posible_taken)] == None:
                        #Check is it oponent 
                        if not board[self.convert_to_alpha(posible_taken)].team == team:
                            takens.append(posible_taken)
            
            alpha_takens = []
            for taken in takens:
                alpha_takens.append(self.convert_to_alpha(taken))
            
            return alpha_takens

        def ability(self, start, board, team):
            # moves forward for each team
            if team == 'white':
                deltas = [[0, 1]]
            else:
                deltas = [[0,-1]]

            # Dubble first move
            if self.turn == 0:
                mrange = 2
            else:
                mrange = 1
            
            self.turn += 1

            alpha_moves, alpha_takens = self.posible_moves(start, board, team, deltas, mrange)
            alpha_takens = self.posible_taken(start, board, team)
            return alpha_moves, alpha_takens


def main():
    Chess()


if __name__ == '__main__':
    main()
