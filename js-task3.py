import sys
import random
import hmac
import hashlib
from tabulate import tabulate


class CryptoUtils:
    @staticmethod
    def generate_key():
        return ''.join(random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789') for _ in range(32))

    @staticmethod
    def calculate_hmac(key, move):
        hmac_key = key.encode()
        move_bytes = move.encode()
        hmac_value = hmac.new(hmac_key, move_bytes, hashlib.sha3_256).hexdigest()
        return hmac_value

class GameRules:
    @staticmethod
    def get_result(player_move, computer_move, moves):
        player_index = moves.index(player_move)
        computer_index = moves.index(computer_move)
        moves_count = len(moves)
        half_moves_count = moves_count // 2

        if player_index == computer_index:
            return "Draw"
        elif (player_index - computer_index) % moves_count <= half_moves_count:
            return "Win"
        else:
            return "Lose"

class HelpTable:
    def generate_results_table(moves):
        results = []
        for move in moves:
            row = []
            for opponent_move in moves:
                result = GameRules.get_result(move, opponent_move, moves)
                row.append(result)
            results.append(row)
        return results

    @staticmethod
    def display(moves):
        results = HelpTable.generate_results_table(moves)
        table = [[moves[i]] + results[i] for i in range(len(moves))]
        headers = [""] + moves
        print(tabulate(table, headers=headers, tablefmt="grid"))

class Game:
    def __init__(self, moves):
        self.moves = moves

    def play(self):
        key = CryptoUtils.generate_key()
        computer_move = random.choice(self.moves)
        hmac_value = CryptoUtils.calculate_hmac(key, computer_move)
        print("HMAC:", hmac_value)

        print("Available moves:")
        for i, move in enumerate(self.moves):
            print(i + 1, "-", move)
        print("0 - exit")
        print("? - help")

        while True:
            player_input = input("Enter your move: ")
            if player_input == '?':
                HelpTable.display(self.moves)
            elif player_input == '0':
                break
            elif player_input.isdigit() and 1 <= int(player_input) <= len(self.moves):
                player_move = self.moves[int(player_input) - 1]
                print("Your move:", player_move)
                print("Computer move:", computer_move)
                result = GameRules.get_result(player_move, computer_move, self.moves)
                print("You", result + "!")
                print("HMAC key:", key)
                break
            else:
                print("Invalid input. Please try again.")


if __name__ == '__main__':
    moves = sys.argv[1:]
    number_of_moves = len(moves)
    if number_of_moves < 3 or number_of_moves % 2 == 0:
        print("Invalid number of arguments. Please specify an odd number of moves greater than one.")
    else:
        game = Game(moves)
        game.play()
