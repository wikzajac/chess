"""chess.py: chess game"""
__author__ = "Wiktor Zajac"
__license__ = "MIT"
__version__ = "1.0"
__status__ = "production"

import re


class Chess:
    """Chess board as dictionaries"""

    def __init__(self):
        """
        Constructor method
        """

        # History of moves in order <piece> <start position> <end position>
        self.moves = []

        # Moves counter
        self.count = 0

        # Initiates board
        self.board_init()

        # Initiates starting positions on board
        self.setup()

        # Main players combat
        self.game()

        # Print notation
        self.print_notation()

    @property
    def board(self):
        """board getter and setter"""
        return self._board

    @board.setter
    def board(self, board):
        self._board = board

    @property
    def count(self):
        """count getter and setter"""
        return self._count

    @count.setter
    def count(self, count):
        self._count = count

    @property
    def moves(self):
        """moves getter and setter"""
        return self._moves

    @moves.setter
    def moves(self, moves):
        self._moves = moves

    def board_init(self):
        """
        Create chess board
        keys coordinates from coordinates_list

        :return: A dict
        :rtype: dict
        """
        coordinates_list = []
        for i in ["a", "b", "c", "d", "e", "f", "g", "h"]:
            for j in range(1, 9):
                coordinates_list.append(i + str(j))
        self.board = dict.fromkeys(coordinates_list)

    def setup(self):
        """
        Set up chess board
        board dictionary store piece as value

        :return: A dict
        :rtype: dict
        """

        # Setup white pieces
        self.board["e1"] = self.King("white")
        self.board["d1"] = self.Queen("white")
        for pos in ["a1", "h1"]:
            self.board[pos] = self.Rook("white")
        for pos in ["c1", "f1"]:
            self.board[pos] = self.Bishop("white")
        for pos in ["b1", "g1"]:
            self.board[pos] = self.Knight("white")
        for pos in ["a2", "b2", "c2", "d2", "e2", "f2", "g2", "h2"]:
            self.board[pos] = self.Pawn("white")

        # Setup black pieces
        self.board["e8"] = self.King("black")
        self.board["d8"] = self.Queen("black")
        for pos in ["a8", "h8"]:
            self.board[pos] = self.Rook("black")
        for pos in ["c8", "f8"]:
            self.board[pos] = self.Bishop("black")
        for pos in ["b8", "g8"]:
            self.board[pos] = self.Knight("black")
        for pos in ["a7", "b7", "c7", "d7", "e7", "f7", "g7", "h7"]:
            self.board[pos] = self.Pawn("black")

    def print_board(self):
        """
        Function print current board in terminal

        """
        # Print upper line with alphabetic coordinate
        print("  ", end="")
        for i in ["a", "b", "c", "d", "e", "f", "g", "h"]:
            print(f" {i} ", end="")
        print("  ")

        # Print board with piece and numeric coordinate
        for j in range(8, 0, -1):
            print(f" {j}", end="")
            for k in ["a", "b", "c", "d", "e", "f", "g", "h"]:
                pos = k + str(j)
                if self.board[pos] is None:
                    print("   ", end="")
                else:
                    print(f" {self.board[pos]} ", end="")
            print(f" {j}")

        # Print lower line with alphabetic coordinate
        print("  ", end="")
        for i in ["a", "b", "c", "d", "e", "f", "g", "h"]:
            print(f" {i} ", end="")
        print("  ")

    def team_round(self):
        """
        Function check current team
        """
        if self.count % 2 == 0:
            team = "white"
        else:
            team = "black"
        return team

    def prompt(self):
        """
        Prompt user for move or exit programm
        Check:
            correct command
            correct piece name
            correct coordinate

            :return list of strings [piece, start, end, team]
            :rtype list
        """

        # Team tracking
        team = self.team_round()

        # Checking player order to move
        # Accept only: <piece> <start position> <end position>. e.g. king e1 f2
        while True:
            try:
                # end game by exit commend
                prompt = input(f"{team} move: ")
                if prompt == "exit":
                    return "exit"
                piece, start, end = prompt.lower().split()
            except ValueError:
                print("Invalid input")
                print("Usage: <piece> <start position> <end position>")
                print("e.g. pawn a2 a4")
                break

            # Accept only correct piece name
            if piece not in ["king", "queen", "rook", "bishop", "knight", "pawn"]:
                print(f"{piece} is not chess piece")
                print("Usage: king, queen, rook, bishop, knight, pawn")
                break

            # Accept only correct coordinate
            match = re.search("[a-h][1-8]", start)
            if not match:
                print(f"{match} is not chess coordinate")
                print("Usage: [a-h][1-8] e.g. f6")
                break

            # Accept only correct coordinate
            match = re.search("[a-h][1-8]", end)
            if not match:
                print(f"{match} is not chess coordinate")
                print("Usage: [a-h][1-8] e.g. f6")
                break

            if self.board[start] is None:
                print(f"There is no {piece} in here")
                break

            if self.board[start] == self.board[end]:
                print("Start square can not be the same as end square")
                break

            # Accept only current team pieces
            if not self.board[start].team == team:
                print(f"This {piece} is not yours")
                break

            # Move piece with correct name
            if not self.board[start].character == piece:
                print(f"{piece} is not in {start}")
                break
            return [piece, start, end, team]
        return 1

    def move(self):
        """
        Function moves pieces on board. Input take from prompt function.
        Analize by ability function is it posible to get end position.
        Piece can make move or capture oponent piece.
        """

        prompt = self.prompt()
        if prompt == "exit":
            return "exit"

        if prompt == 1:
            return 1

        piece, start, end, team = prompt

        posibility_moves, posibility_takens = self.board[start].ability(
            start, self.board, team
        )
        if end in posibility_moves:
            step = self.board[start]
            self.board[end] = step
            self.board[start] = None

            # Add move to history
            stage = f"{piece} {start} {end}"
            self.moves.append(stage)
            self.count += 1
            return None
        if end in posibility_takens:
            step = self.board[start]
            self.board[end] = step
            self.board[start] = None

            # Add move to history
            stage = f"{piece} {start} {end}"
            self.moves.append(stage)
            self.count += 1
            return None
        print(f"{piece} can not do that for you")
        return 1

    def game(self):
        """
        Function generate loop of moves and printing board till exit command
        """

        while True:
            self.print_board()
            if self.move() == "exit":
                break

    def print_notation(self):
        """
        Function print all moves in game
        """
        if not self.moves:
            print("No moves")
        else:
            for line in self.moves:
                print(line)

    class Piece:
        """
        Main class for all pieces in board
        """

        def __init__(self, team, character):
            self.team = team
            self.character = character

        def __str__(self):
            return f"{self.team} {self.character}"

        @property
        def team(self):
            """team getter and setter"""
            return self._team

        @team.setter
        def team(self, team):
            if team not in ["white", "black"]:
                raise ValueError("Invalid team")
            self._team = team

        @property
        def character(self):
            """character getter and setter"""
            return self._character

        @character.setter
        def character(self, character):
            characters = ["king", "queen", "rook", "bishop", "knight", "pawn"]
            if character not in characters:
                raise ValueError("Invalid character")
            self._character = character

        def convert_to_numeric(self, pos):
            """
            Convert clasic chess coordinates to numeric coordinates
            e.g. d4 to [4, 4]
            :return numeric coordinate
            :rtype list of two intiger
            """
            num = ord(pos[0]) - 96
            return [num, int(pos[1])]

        def convert_to_alpha(self, pos):
            """
            Convert numeric coordinates to clasic chess coordinates
            e.g. [4, 4] to d4
            :return clasic chees coordinates
            :rtype string
            """
            alpha = chr(int(pos[0]) + 96)
            return alpha + str(pos[1])

        def sum_coordinates(self, pos1, pos2):
            """
            add numeric coordinates and delta
            :return sum of coordinates
            :rtype list of two intiger
            """
            pos3 = []
            pos3.append(pos1[0] + pos2[0])
            pos3.append(pos1[1] + pos2[1])
            return pos3

        def is_it_in_board(self, pos_numeric):
            """
            Check if coordinates is in board
            e.g. [1, 1] -> True, [9, 8] -> False
            :rtype boolean
            """
            if pos_numeric[0] > 0:
                if pos_numeric[0] < 9:
                    if pos_numeric[1] > 0:
                        if pos_numeric[1] < 9:
                            return True
            return False

        def posible_moves(self, start, board, team, deltas, mrange):
            """
            Check posible moves or posible taken for piece
            :return two list of clasic chess coordinates.
            :rtype list of strings
            """

            start_numeric = self.convert_to_numeric(start)
            moves = []
            takens = []
            for delta in deltas:
                step = [None, None]
                step[0] = int(delta[0])
                step[1] = int(delta[1])
                copy_mrange = mrange
                while copy_mrange != 0:
                    # piece range
                    copy_mrange = mrange - 1
                    # move one step
                    posible_position = self.sum_coordinates(start_numeric, step)
                    posible_position_alpha = self.convert_to_alpha(posible_position)

                    # step for next iteration
                    step[0] = step[0] + delta[0]
                    step[1] = step[1] + delta[1]

                    # check is it in board
                    if self.is_it_in_board(posible_position):
                        pass
                    else:
                        break
                    # check is it None
                    if board[posible_position_alpha] is None:
                        moves.append(posible_position)
                    elif not board[posible_position_alpha].team == team:
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
        """King piece"""

        def __init__(self, team, character="king"):
            super().__init__(team, character)

        def __str__(self):
            if self.team == "white":
                return "♔"
            return "♚"

        def ability(self, start, board, team):
            """
            Check ability for taken and moves.
            Variable with piece range and piece directions
            """
            deltas = [
                [1, 1],
                [0, 1],
                [-1, 1],
                [-1, 0],
                [-1, -1],
                [0, -1],
                [1, -1],
                [1, 0],
            ]
            mrange = 1
            alpha_moves, alpha_takens = self.posible_moves(
                start, board, team, deltas, mrange
            )

            return alpha_moves, alpha_takens

    class Queen(Piece):
        """Queen piece"""

        def __init__(self, team, character="queen"):
            super().__init__(team, character)

        def __str__(self):
            if self.team == "white":
                return "♕"
            return "♛"

        def ability(self, start, board, team):
            """
            Check ability for taken and moves.
            Variable with piece range and piece directions
            """
            deltas = [
                [1, 1],
                [0, 1],
                [-1, 1],
                [-1, 0],
                [-1, -1],
                [0, -1],
                [1, -1],
                [1, 0],
            ]
            mrange = 8
            alpha_moves, alpha_takens = self.posible_moves(
                start, board, team, deltas, mrange
            )

            return alpha_moves, alpha_takens

    class Rook(Piece):
        """Rook piece"""

        def __init__(self, team, character="rook"):
            super().__init__(team, character)

        def __str__(self):
            if self.team == "white":
                return "♖"
            return "♜"

        def ability(self, start, board, team):
            """
            Check ability for taken and moves.
            Variable with piece range and piece directions
            """
            deltas = [[0, 1], [-1, 0], [0, -1], [1, 0]]
            mrange = 8
            alpha_moves, alpha_takens = self.posible_moves(
                start, board, team, deltas, mrange
            )

            return alpha_moves, alpha_takens

    class Bishop(Piece):
        """Bishop piece"""

        def __init__(self, team, character="bishop"):
            super().__init__(team, character)

        def __str__(self):
            if self.team == "white":
                return "♗"
            return "♝"

        def ability(self, start, board, team):
            """
            Check ability for taken and moves.
            Variable with piece range and piece directions
            """
            deltas = [[1, 1], [1, -1], [-1, 1], [-1, -1]]
            mrange = 8
            alpha_moves, alpha_takens = self.posible_moves(
                start, board, team, deltas, mrange
            )
            return alpha_moves, alpha_takens

    class Knight(Piece):
        """Knight piece"""

        def __init__(self, team, character="knight"):
            super().__init__(team, character)

        def __str__(self):
            if self.team == "white":
                return "♘"
            return "♞"

        def ability(self, start, board, team):
            """
            Check ability for taken and moves.
            Variable with piece range and piece directions
            """
            deltas = [
                [1, 2],
                [2, 1],
                [2, -1],
                [1, -2],
                [-1, -2],
                [-2, -1],
                [-2, 1],
                [-1, 2],
            ]
            mrange = 1
            alpha_moves, alpha_takens = self.posible_moves(
                start, board, team, deltas, mrange
            )

            return alpha_moves, alpha_takens

    class Pawn(Piece):
        """Pawn piece"""

        def __init__(self, team, character="pawn"):
            super().__init__(team, character)

            self.turn = 0

        def __str__(self):
            if self.team == "white":
                return "♙"
            return "♟"

        @property
        def turn(self):
            """turn getter and setter"""
            return self._turn

        @turn.setter
        def turn(self, turn):
            self._turn = turn

        def posible_taken(self, start, board, team):
            """
            Check posible posible taken for pawn
            :return list of clasic chess coordinates.
            :rtype list of strings
            """
            start_numeric = self.convert_to_numeric(start)
            takens = []
            if team == "white":
                deltas = [[-1, 1], [1, 1]]
            else:
                deltas = [[1, -1], [-1, -1]]

            for delta in deltas:
                posible_taken = self.sum_coordinates(start_numeric, delta)
                posible_taken_alpha = self.convert_to_alpha(posible_taken)
                # check is it in board
                if self.is_it_in_board(posible_taken):
                    # Check is it empty square
                    if not board[posible_taken_alpha] is None:
                        # Check is it oponent
                        if not board[posible_taken_alpha].team == team:
                            takens.append(posible_taken)

            alpha_takens = []
            for taken in takens:
                alpha_takens.append(self.convert_to_alpha(taken))

            return alpha_takens

        def ability(self, start, board, team):
            """
            Check ability for taken and moves.
            Variable with piece range and piece directions
            """
            if team == "white":
                deltas = [[0, 1]]
            else:
                deltas = [[0, -1]]

            # Dubble first move
            if self.turn == 0:
                mrange = 2
            else:
                mrange = 1

            self.turn += 1

            alpha_moves, alpha_takens = self.posible_moves(
                start, board, team, deltas, mrange
            )
            alpha_takens = self.posible_taken(start, board, team)
            return alpha_moves, alpha_takens


def main():
    """Iniciacion Chess class"""
    Chess()


if __name__ == "__main__":
    main()
